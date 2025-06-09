from agents import Agent
from ..tools.get_tinh_huong_tool import get_tinh_huong

from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
Bạn là chuyên gia làm rõ tình huống. Nhiệm vụ của bạn:
- Phân tích và giải thích đơn giản, rõ ràng về tình huống đã đưa ra
- Chỉ giải thích về tình huống, KHÔNG đưa ra hướng xử lý
- Nội dung phải kết nối tự nhiên với mạch trò chuyện hiện tại
- Giữ phong cách như 2 người đang trò chuyện thân thiện
''')

clarification_agent = Agent(
    name="AgentLamRongTinhHuong",
    handoff_description="Chuyên gia giải thích và làm rõ các tình huống khi người dùng chưa hiểu",
    instructions=instructions,
    tools=[get_tinh_huong],
    handoffs=[],
    model="gpt-4o-mini"
)
