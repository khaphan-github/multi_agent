from agents import RunContextWrapper, function_tool
from ..models.models import CustomContexModel


@function_tool
async def get_chat_history(wrapper: RunContextWrapper[CustomContexModel]) -> str:
    '''
    Lấy lịch sử trò chuyện của người dùng
    '''
    history = wrapper.context.history
    r = f"Lịch sử trò chuyện là:\n{history}"
    return r
