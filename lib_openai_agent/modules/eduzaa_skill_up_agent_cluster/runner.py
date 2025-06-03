from typing import AsyncGenerator
from agents import Runner, trace
from openai.types.responses import ResponseTextDeltaEvent

from .contexts.context import *
from .tools import *
from .models import *
from .agents import *

# region get thong tin bo xugn cho model
# https://openai.github.io/openai-agents-python/tools/


async def run_skillup_conversation(user_input: str, context) -> AsyncGenerator[str, None]:
    with trace(workflow_name="Conversation", group_id='1'):
        result = await Runner.run(triage_agent, user_input, context=context)
        print(result)
        new_input = result.to_input_list()
        result = Runner.run_streamed(generate_response_agent, new_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                yield delta
