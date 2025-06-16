from openai import AsyncOpenAI as OpenAI
from .utils.pooling_event import ProcessEventPolling
from .utils.thread import *
from .constant import *
from .openai_config import OpenAILLMConfig
from ..model.llm_message import LLMMessage, Role
from ..model.llm_service_base import LLMServiceBase  # Updated import
from ..model.llm_message import LLMMessageHandler


class OpenAIService(LLMServiceBase):  # Updated base class
    def __init__(self, config: OpenAILLMConfig, message_handler: LLMMessageHandler = None):
        super().__init__(config)
        self.polling_event = ProcessEventPolling(config.tool_instances)
        self.client = OpenAI(api_key=config.api_key)
        self.message_handler = message_handler  # Initialize message handler

        if self.config.use_message and self.message_handler is None:
            from ..shared.history.message_history_redis_impl import LLMMessageHandlerImpl
            self.message_handler = LLMMessageHandlerImpl()

    async def push_mgs(self, message):
        """
        Push a message to the message handler.
        """
        if self.config.use_message and self.message_handler:
            self.message_handler.push_message(message)

    async def chat(self, content):
        '''
            Kiem tra dieu kien
            - Enable
            - Budget
            Neu thoa thi moi thuc hien
        '''
        self.can_use()
        max_token_limit = self.get_max_token_limit()
        user_message = LLMMessage(role=Role.USER, message=content)
        await self.push_mgs(user_message)  # Push user message

        try:
            response = await self.client.completions.create(
                model=self.config.model,
                prompt=content,
                max_tokens=max_token_limit,
                temperature=self.config.temperature,
            )

            await self.usaged_budget_token(total_token=response.usage.total_tokens)

            assistant_message = LLMMessage(
                role=Role.AI, message=response.choices[0].text)

            await self.push_mgs(assistant_message)  # Push assistant message

            return response.choices[0].text

        except Exception as e:
            print(f"OpenAIProxy: Error in chat: {e}")

    async def chat_stream(self, content):
        '''
            Kiểm tra điều kiện:
            - Enable
            - Budget
            Nếu thỏa thì mới thực hiện
        '''
        self.can_use()
        max_token_limit = self.get_max_token_limit()
        user_message = LLMMessage(role=Role.USER, message=content)
        await self.push_mgs(user_message)  # Push user message

        try:
            total_token = 0
            stream = await self.client.completions.create(
                model=self.config.model,
                prompt=content,
                max_tokens=max_token_limit,
                temperature=self.config.temperature,
                stream=True,
            )

            assistant_content = ""
            async for response in stream:
                # Extract text from the streamed response
                text = response.choices[0].text if response.choices and response.choices[0].text else ''
                assistant_content += text
                yield text

                # Update token count if available
                if hasattr(response, "usage") and response.usage and response.usage.total_tokens:
                    total_token = response.usage.total_tokens

            await self.usaged_budget_token(total_token=total_token)

            assistant_message = LLMMessage(
                role=Role.AI,
                message=assistant_content
            )

            await self.push_mgs(assistant_message)  # Push assistant message

        except Exception as e:
            print(f"OpenAIProxy: Error in chat_stream: {e}")
