from agents import Agent
from ..tools import *
from ..models.models import HintAgentOutput

from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
Bạn là chuyên gia đưa ra gợi ý. 
Nhiệm vụ của bạn:
- Đưa ra 1-2 ý tưởng chung chung, không nói rõ ràng cách giải quyết cụ thể
''')

hint_agent = Agent(
    name="AgentGoiY",
    handoff_description="Chuyên gia đưa ra gợi ý nhỏ",
    instructions=instructions,
    output_type=HintAgentOutput,
    tools=[get_tinh_huong]
)
