from agents import Agent
from ..tools import get_chat_history
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent
from .unanwser_agent import unanwser_agent

triage_agent = Agent(
    name="Agent Phân loại",
    # model="gpt-4.1",
    instructions="""Bạn là Agent điều phối chịu trách nhiệm phân tích và chuyển tiếp người dùng đến agent phù hợp.
    Quy tắc chuyển tiếp:
    - Người dùng không thể giải quyết vấn đề, cần hỗ trợ cảm xúc,  Người dùng tỏ ra lo lắng, thất vọng, hoặc cần động viên  -> Chuyển sang Agent Tâm Lý (unanwser_agent)
    - Người dùng cần gợi ý khi chưa có ý tưởng xử lý -> Chuyển sang Agent Gợi ý (hint_agent)
    - Người dùng yêu cầu giải thích tình huống không rõ ràng -> Chuyển sang Agent Làm rõ tình huống (clarification_agent)
    - Người dùng trả lời đủ mức để đưa ra nhận xét và giải pháp -> Chuyển sang Agent Giải pháp Hệ thống (solution_agent)

    """,
    handoffs=[clarification_agent, hint_agent, solution_agent, unanwser_agent],
    tools=[get_chat_history],
)
