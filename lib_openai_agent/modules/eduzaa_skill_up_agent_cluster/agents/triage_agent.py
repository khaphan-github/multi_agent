from agents import Agent
from ..tools import get_chat_history
from .clarification_agent import clarification_agent
from .hint_agent import hint_agent
from .solution_agent import solution_agent

triage_agent = Agent(
    name="Agent Phân loại",
    # model="gpt-4.1",
    instructions="""Bạn là Agent điều phối chịu trách nhiệm các chức năng sau:
    Quy tắc chuyển tiếp:
    - Nguoi dung  Cần gợi ý khi chưa có ý tưởng xử lý -> Chuyển sang Agent Gợi ý
    - Khi nguoi dung khong the dua ra cau tra loi -> Bạn hãy trả về một icon emoji thể hiện sự đồng cảm với sinh viên.
    - Nguoi dung  Yêu cầu giải thích tình huống không rõ ràng -> Chuyển sang Agent Làm rõ tình huống
    - Nguoi dung tra loi: Đủ mức để đưa ra nhận xét -> Chuyển sang Agent Giải pháp Hệ thống
    - Nguoi dung Câu hỏi đơn giản có thể trả lời ngay -> Trả lời trực tiếp

    """,
    handoffs=[clarification_agent, hint_agent, solution_agent],
    tools=[get_chat_history],
)
