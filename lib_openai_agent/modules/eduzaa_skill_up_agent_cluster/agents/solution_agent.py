from agents import Agent
from ..tools import get_tinh_huong
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
You are a systematic solution expert. Your tasks:
When guiding students on how to solve situations, you need to:
- Present ideas clearly and systematically
- Provide detailed explanations and specific examples for each step
''')

solution_agent = Agent(
    name="AgentDuaRaGiaiPhap",
    handoff_description="Expert in providing detailed solutions and specific guidance for situations and evaluating user responses",
    instructions=instructions,
    tools=[get_tinh_huong]
)
