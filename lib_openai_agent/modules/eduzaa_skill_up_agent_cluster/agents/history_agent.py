from agents import Agent
from ..tools import *
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

instructions = prompt_with_handoff_instructions('''
Đây là Agent có khả năng tương tác với lịch sử cuộc hội thoại. 
Agent này có thể truy xuất và sử dụng thông tin từ các cuộc hội thoại trước đó để hỗ trợ trong các tình huống hiện tại.
''')
history_agent = Agent(
  name="AgentTuongTacGhiNhoCuocHoiThoai",
  instructions=instructions,
  handoffs=[],
  tools=[get_chat_history],
)
