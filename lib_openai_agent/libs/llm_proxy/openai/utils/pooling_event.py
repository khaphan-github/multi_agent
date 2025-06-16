from core.singleton import Singleton
from openai import AsyncOpenAI as OpenAI
from openai.types.beta import Thread
from openai.types.beta.assistant_stream_event import (
    ThreadRunRequiresAction,
    ThreadMessageDelta,
    ThreadRunFailed,
    ThreadRunCancelling,
    ThreadRunCancelled,
    ThreadRunExpired,
    ThreadRunStepFailed,
    ThreadRunStepCancelled,
)
import asyncio
import json

'''
Cho Asisstant
   - Nhan event tu openai - cac trang thai xu ly cua RUN (thread + messsage)
   - Gom token tu stream message va stream tu tool call
'''


class ProcessEventPolling():
    tool_instances = {}

    def __init__(self, tool_instances=None):
        """
        """
        self.tool_instances = tool_instances

    def create_tool_output(self, tool_call, tool_result):
        """
        This function creates the tool output.
        """
        output = {
            "tool_call_id": tool_call.id,
            "output": tool_result,
        }
        return output

    async def process_event(self, client: OpenAI, event, thread: Thread, **kwargs):
        """
        Process an event in the thread.

        Args:
            event: The event to be processed.
            thread: The thread object.
            **kwargs: Additional keyword arguments.

        Yields:
            The processed tokens.

        Raises:
            Exception: If the run fails.
        """
        if isinstance(event, ThreadMessageDelta):
            data = event.data.delta.content
            for d in data:
                yield d

        elif isinstance(event, ThreadRunRequiresAction):
            run_obj = event.data
            tool_outputs = await self.process_tool_calls(
                run_obj.required_action.submit_tool_outputs.tool_calls
            )
            tool_output_events = (
                await client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run_obj.id,
                    tool_outputs=tool_outputs,
                    stream=True,
                )
            )
            async for tool_event in tool_output_events:
                async for token in self.process_event(
                    client=client,
                    event=tool_event,
                    thread=thread,
                    **kwargs
                ):
                    yield token

        elif any(
            isinstance(event, cls)
            for cls in [
                ThreadRunFailed,
                ThreadRunCancelling,
                ThreadRunCancelled,
                ThreadRunExpired,
                ThreadRunStepFailed,
                ThreadRunStepCancelled,
            ]
        ):
            raise Exception(
                "Run failed")  # pylint: disable=broad-exception-raised

    async def process_tool_call(self, tool_call, tool_outputs: list, extra_args=None):
        """
        This function processes a single tool call.
        And also handles the exceptions.
        """
        result = None
        try:
            arguments = json.loads(tool_call.function.arguments)
            function_name = tool_call.function.name
            if extra_args:
                for key, value in extra_args.items():
                    arguments[key] = value
            if function_name not in self.tool_instances:
                result = "Tool not found"
            else:
                result = await self.tool_instances[function_name](**arguments)
        except Exception as e:  # pylint: disable=broad-except
            result = str(e)
            print('process_tool_call', e)
        created_tool_output = self.create_tool_output(tool_call, result)
        tool_outputs.append(created_tool_output)

    async def process_tool_calls(self, tool_calls, extra_args=None):
        """
        This function processes all the tool calls.
        """
        tool_outputs = []
        coroutines = []
        total_calls = len(tool_calls)
        for i in range(total_calls):
            tool_call = tool_calls[i]
            coroutines.append(self.process_tool_call(
                tool_call, tool_outputs, extra_args))
        if coroutines:
            await asyncio.gather(*coroutines)
        return tool_outputs
