from agents import Agent, WebSearchTool

from ..tools import *
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
This is a Knowledge Agent capable of managing and retrieving information.
This agent can access, organize, and provide knowledge from various sources to assist users with their questions and tasks.
It specializes in finding relevant information and presenting it in a clear, useful manner.
''')
knowledge_agent = Agent(
    name="AgentQuanLyKienThuc",
    instructions=instructions,
    handoff_description="Expert in managing and retrieving information",
    handoffs=[],
    tools=[
        WebSearchTool(),
        get_current_time,
    ],
)
