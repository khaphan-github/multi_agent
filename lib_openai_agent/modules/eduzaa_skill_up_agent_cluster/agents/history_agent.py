from agents import Agent
from ..tools import *
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
This is an Agent capable of interacting with conversation history.
This agent can retrieve and use information from previous conversations to assist in current situations.
''')
history_agent = Agent(
    name="AgentTuongTacGhiNhoCuocHoiThoai",
    instructions=instructions,
    handoffs=[],
    tools=[get_chat_history],
)
