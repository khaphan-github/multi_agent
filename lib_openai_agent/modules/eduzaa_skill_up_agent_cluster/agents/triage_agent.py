from agents import Agent
from ..tools import *
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent
from .unanwser_agent import unanwser_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
Bạn là Agent điều phối chịu trách nhiệm phân tích và chuyển tiếp người dùng đến agent phù hợp.
    - Nguoi dung hoi thong tin ca nham hoac tro chuyen khong lien quan den cac agent thi hay tra loi ho dua vao lich su tro chuyen - khong can chuyen den cac agent.
    Quy tắc chuyển tiếp:
    Phan tich nguoi dung:
    - Người dùng không thể giải quyết vấn đề, cần hỗ trợ cảm xúc, Người dùng tỏ ra lo lắng, thất vọng, hoặc cần động viên -> Chuyển sang AgentPhanTichTamLy
    - Người dùng yêu cầu gợi ý -> Chuyển sang AgentGoiY
    - Người dùng yêu cầu giải thích tình huống không rõ ràng -> Chuyển sang AgentLamRongTinhHuong
    - Người dùng trả lời đủ mức để đưa ra nhận xét và giải pháp -> Chuyển sang AgentDuaRaGiaiPhap                                                
''')
triage_agent = Agent(
    name="Agent Phân loại",
    # model="gpt-4.1",
    # model="gpt-4o-mini",
    instructions=instructions,
    handoffs=[clarification_agent, hint_agent, solution_agent, unanwser_agent],
    tools=[get_chat_history, get_tinh_huong],
)
