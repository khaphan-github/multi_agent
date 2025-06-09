from agents import Agent
from ..tools import get_chat_history
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent
from .unanwser_agent import unanwser_agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

triage_agent = Agent(
    name="Agent Phân loại",
    # model="gpt-4.1",
    model="gpt-4o-mini",
    instructions="""
    {RECOMMENDED_PROMPT_PREFIX}
Bạn là Agent điều phối chịu trách nhiệm phân tích và chuyển tiếp người dùng đến agent phù hợp.
    Quy tắc chuyển tiếp:
    Phan tich nguoi dung:
    - Người dùng không thể giải quyết vấn đề, cần hỗ trợ cảm xúc, Người dùng tỏ ra lo lắng, thất vọng, hoặc cần động viên -> Chuyển sang AgentPhanTichTamLy
    - Người dùng yêu cầu gợi ý -> Chuyển sang AgentGoiY
    - Người dùng yêu cầu giải thích tình huống không rõ ràng -> Chuyển sang AgentLamRongTinhHuong
    - Người dùng trả lời đủ mức để đưa ra nhận xét và giải pháp -> Chuyển sang AgentDuaRaGiaiPhap
    """,
    handoffs=[clarification_agent, hint_agent, solution_agent, unanwser_agent],
    tools=[get_chat_history],
)
