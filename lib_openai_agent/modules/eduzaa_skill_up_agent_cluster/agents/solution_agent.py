from agents import Agent
from ..tools import get_tinh_huong
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
Bạn là chuyên gia đưa ra giải pháp hệ thống. Nhiệm vụ của bạn:
Khi cần hướng dẫn sinh viên cách giải quyết tình huống, bạn cần:
- Trình bày các ý một cách rõ ràng, có hệ thống
- Kèm theo giải thích chi tiết và ví dụ cụ thể cho mỗi bước
''')

solution_agent = Agent(
    name="AgentDuaRaGiaiPhap",
    handoff_description="Chuyên gia đưa ra cách giải quyết chi tiết và hướng dẫn cụ thể cho tình huống va danh gia cau tra loi cua nguoi dung",
    instructions=instructions,
    tools=[get_tinh_huong]
)
