from typing import AsyncGenerator
from agents import Runner, trace
from ..contexts.context import *
from ..tools import *
from ..models.models import *
from ..agents import *
# region get thong tin bo xugn cho model
# https://openai.github.io/openai-agents-python/tools/


async def run_skillup_conversation(user_input: str, context) -> AsyncGenerator[str, None]:
    with trace(workflow_name="Conversation"):
        result = await Runner.run(triage_agent, user_input, context=context)
        new_input = result.to_input_list()
        result = Runner.run_streamed(
            generate_response_agent, new_input)
        return result
