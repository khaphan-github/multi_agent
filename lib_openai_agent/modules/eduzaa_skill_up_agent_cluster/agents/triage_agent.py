from agents import Agent
from ..tools import *
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent
from .unanwser_agent import unanwser_agent
from .knowledge_agent import knowledge_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
You are a triage Agent responsible for analyzing and forwarding users to the appropriate agent.
Forwarding rules:
- Users converse and ask for information related to the conversation => transfer_to_AgentQuanLyKienThuc
- Users cannot resolve the issue, need emotional support, appear anxious, frustrated, or need encouragement => transfer_to_AgentPhanTichTamLy
- Users request suggestions => transfer_to_AgentHint
- Users request clarification of unclear situations => transfer_to_AgentLamRoTinhHuong
- Users provide sufficient input to give feedback and solutions => transfer_to_AgentDuaRaGiaiPhap
''')
triage_agent = Agent(
    name="AgentPhanLoai",
    instructions=instructions,
    handoffs=[clarification_agent, hint_agent,
              solution_agent, unanwser_agent, knowledge_agent],
    tools=[],
)
