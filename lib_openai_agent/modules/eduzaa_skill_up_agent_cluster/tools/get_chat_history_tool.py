from agents import RunContextWrapper, function_tool
from ..models import CustomContexModel


@function_tool
async def get_chat_history(wrapper: RunContextWrapper[CustomContexModel]) -> str:
    '''
    Lấy lịch sử trò chuyện của người dùng
    '''
    return f"Lịch sử trò chuyện là: {wrapper.context.history} "
