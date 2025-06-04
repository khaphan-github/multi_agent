from agents import Agent
from ..tools import get_tinh_huong
from ..models.models import HintAgentOutput

hint_agent = Agent(
    name="Agent Gợi ý",
    handoff_description="Chuyên gia đưa ra gợi ý nhỏ khi người dùng chưa có ý tưởng xử lý tình huống",
    instructions="""Bạn là chuyên gia đưa ra gợi ý. Nhiệm vụ của bạn:
Khi sinh viên chưa có ý tưởng xử lý tình huống, bạn cần:
- Đưa ra 1-2 ý tưởng chung chung, không nói rõ ràng cách giải quyết cụ thể
- Giúp sinh viên có hướng suy nghĩ để tự tìm ra cách xử lý phù hợp
""",
    output_type=HintAgentOutput,
    tools=[get_tinh_huong]
)
