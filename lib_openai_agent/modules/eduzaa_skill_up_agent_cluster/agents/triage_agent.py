from agents import Agent
from ..tools import *
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent
from .unanwser_agent import unanwser_agent
from .history_agent import history_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''1
You are a triage Agent responsible for analyzing and forwarding users to the appropriate agent.
    Forwarding rules:
    - Users converse and ask for information related to the conversation => Forward to agent AgentTuongTacGhiNhoCuocHoiThoai
    - Users cannot resolve the issue, need emotional support, appear anxious, frustrated, or need encouragement -> Forward to AgentPhanTichTamLy
    - Users request suggestions -> Forward to AgentGoiY
    - Users request clarification of unclear situations -> Forward to AgentLamRongTinhHuong
    - Users provide sufficient input to give feedback and solutions -> Forward to AgentDuaRaGiaiPhap                                                
''')
triage_agent = Agent(
    name="AgentPhanLoai",
    instructions=instructions,
    handoffs=[clarification_agent, hint_agent,
              solution_agent, unanwser_agent, history_agent],
    tools=[],
)
