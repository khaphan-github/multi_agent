import asyncio
import time
from openai import AsyncOpenAI as OpenAI
from openai.types.beta import Thread
from openai.types.beta.assistant_stream_event import (
    ThreadRunCompleted,
)
from .utils.pooling_event import ProcessEventPolling
from .utils.thread import *
from .constant import *
from .utils.stream import process_message
from ..model.llm_service_base import LLMServiceBase  # Updated import
from libs.utils.u_logger import Logger
from .openai_config import OpenAILLMConfig
from ..model.llm_message import LLMMessageHandler
from ..shared.history.message_history_redis_impl import LLMMessageHandlerImpl
from ..model.llm_message import LLMMessage
from ..model.llm_message import Role

'''
How to use this class
1. Create an instance of OpenAIAssistantProxy with the required configuration.
2. Call the `assistant_chat` method with the content you want to send to the assistant.
3. The method will return the assistant's response.
5. Example code:
'''


class OpenAIAssistantService(LLMServiceBase):  # Updated base class
    def __init__(self, config: OpenAILLMConfig, message_handler: LLMMessageHandler = None):
        '''
        History:
            neu muon cutom message handler thi implement LLMMessageHandler
            class LLMMessageHandlerImpl(LLMMessageHandler):
                def __init__(self):
                ...
            Mac dinh neu enable message handle ler thi no luwu trong redis
        '''
        super().__init__(config)
        self.client = OpenAI(api_key=config.api_key)
        self.polling_event = ProcessEventPolling(
            tool_instances=config.tool_instances)
        # [ISSUE-01] Dont need set message handler here is none.
        # self.message_handler = None  # Initialize to None

        if self.config.use_message == True:
            if message_handler is None:
                self.message_handler = LLMMessageHandlerImpl()
            else:
                self.message_handler = message_handler
        else:
            self.message_handler = None

    async def push_mgs(self, message: LLMMessage):
        """
        Push a message to the message handler.
        """
        # [ISSUE-01] Dont need set message handler here is none.
        if self.config.use_message == True:
            self.message_handler.push_message(message)

    async def validate_exist_assistant(self):
        """
        Retrieve an assistant by its ID.
        """
        if not self.config.assistant_id:
            raise ValueError("Assistant ID is not set in the config.")
        try:
            assistant = await self.client.beta.assistants.retrieve(self.config.assistant_id)
            if assistant is None:
                raise ValueError(
                    f"Assistant with ID {self.config.assistant_id} does not exist.")
            return assistant
        except Exception as e:
            raise Exception(f"Error retrieving assistant: {e}")

    # truyen vo key chat -> get thread_id trong redis ->

    async def assistant_chat(self, content, thread_key=None, metadata=None):
        try:
            await self.can_use()
            max_token_limit = await self.get_max_token_limit()

            # Create or retrieve the thread
            thread_id = await create_thread(self.client, thread_key)

            # Step 1: Get the ID of the last message before the run
            previous_messages = await self.client.beta.threads.messages.list(
                thread_id=thread_id,
                order='desc',
                limit=1
            )
            last_message_id_before_run = previous_messages.data[
                0].id if previous_messages.data else None

            # Step 2: Add user message to the thread
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content,
            )

            # Add user message to the handler
            user_message = LLMMessage(
                role=Role.USER,
                message=content,
                metadata=metadata
            )
            await self.push_mgs(user_message)

            # Step 3: Initiate the assistant run
            # TODO: create_and_run use this for best performance
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.config.assistant_id,
                max_prompt_tokens=max_token_limit,
                stream=False,
            )

            # Step 4: Poll for run completion
            while True:
                run_status = await self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id)
                if run_status.status == 'completed':
                    break
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    raise Exception(
                        f"Run ended with status: {run_status.status}")
                await asyncio.sleep(0.5)  # Wait before polling again

            # Step 5: Retrieve messages added after the previous last message
            if last_message_id_before_run:
                new_messages = await self.client.beta.threads.messages.list(
                    thread_id=thread_id,
                    order='asc',
                    after=last_message_id_before_run
                )
            else:
                new_messages = await self.client.beta.threads.messages.list(
                    thread_id=thread_id,
                    order='asc'
                )

            # Step 6: Find the assistant's message
            assistant_message_data = next(
                (msg for msg in new_messages.data if msg.role == 'assistant'),
                None
            )

            if assistant_message_data:
                assistant_content = assistant_message_data.content[0].text.value
                # Push assistant's response to the message handler
                assistant_message = LLMMessage(
                    role=Role.AI,
                    message=assistant_content,
                    usage=run.usage,  # Update if usage data is available
                    metadata=metadata
                )
                await self.push_mgs(assistant_message)
            else:
                assistant_content = "No assistant reply found."

            await self.usaged_budget_token(
                total_token=run_status.usage.total_tokens,
            )

            # Remove the thread if it was newly created
            if not thread_key:
                await remove_thread(self.client, thread_id)

            return assistant_content, thread_id

        except Exception as e:
            Logger.log(f"Error in assistant_chat: {e}")
            return None

    async def default_assistant_chat_stream(self, content, thread_key=None, metadata=None, stream_formater=process_message):
        '''
         content: str: Noi dung chat
         thread_key: str: Neu muon giu boi canh cu thi truyen vao.
             thoi_gian_song cua thread mac dinh la bao lau: 1h

         Chat:
           - Tao thread -> thread_id.
                 -  thread_key = None => Tao thread moi
                 -  Else = retrival thread_id.
             - TODO: Luu lai key trong redis.
           - To user message
           - Theem message vao thread.
           - Goi run - stream ket qua ve.

           - Xoa thread neu khong truyen vao.
             - Xoa khi thread_id.
        '''
        # Create a new thread or retrieve an existing thread
        try:
            await self.can_use()
            max_token_limit = await self.get_max_token_limit()

            thread_id = await create_thread(self.client, thread_key)

            # Add user message to the handler
            user_message = LLMMessage(
                role=Role.USER,
                message=content,
                metadata=metadata
            )
            if self.message_handler is not None:  # Check before using
                self.message_handler.push_message(user_message)

            # Add user message to the thread
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content,
            )
            thread = Thread(id=thread_id, created_at=0,
                            object="thread", metadata={})

            # Stream the assistant's response
            stream = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.config.assistant_id,
                max_prompt_tokens=max_token_limit,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                stream=True,
            )

            total_token = 0
            usage = None
            assistant_content = ""  # Initialize content accumulator

            async for event in stream:
                # Update max token when complete
                if isinstance(event, ThreadRunCompleted):
                    total_token = event.data.usage.total_tokens
                    usage = event.data.usage

                # Extract content from the event and concatenate
                if hasattr(event, 'data') and hasattr(event.data, 'delta'):
                    delta = event.data.delta
                    if hasattr(delta, 'content') and delta.content:
                        for block in delta.content:
                            if block.type == 'text' and block.text.value:
                                assistant_content += block.text.value

                async for token in self.polling_event.process_event(self.client, event, thread):
                    yield stream_formater(token, False, thread_id) if stream_formater else token
                    await asyncio.sleep(0.00000001)

            # Push the concatenated assistant message to the message handler
            if assistant_content:
                assistant_message = LLMMessage(
                    role=Role.AI,
                    message=assistant_content,
                    usage=usage,
                    metadata=metadata
                )
                if self.message_handler is not None:  # Check before using
                    await self.push_mgs(assistant_message)

            # Danh dau message end.
            yield stream_formater('', True, thread_id) if stream_formater else token

            if not thread_key:
                await remove_thread(self.client, thread_id)

            # TODO: Implement buget
            await self.usaged_budget_token(
                total_token=total_token,
            )
        except Exception as e:
            Logger.log(f"Error in default_assistant_chat_stream: {e}")
