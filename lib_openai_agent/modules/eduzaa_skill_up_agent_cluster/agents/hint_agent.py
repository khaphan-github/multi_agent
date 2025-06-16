from agents import Agent
from ..tools import *
from ..models.models import HintAgentOutput

from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
You are a suggestion expert.
Your task:
- Provide 1-2 general ideas, without specifying a clear solution
- you can use get_tinh_huong tool to retrieve the situation context

''')

hint_agent = Agent(
    name="AgentHint",
    handoff_description="Expert providing small suggestions and hints",
    instructions=instructions,
    output_type=HintAgentOutput,
    tools=[get_tinh_huong]
)
