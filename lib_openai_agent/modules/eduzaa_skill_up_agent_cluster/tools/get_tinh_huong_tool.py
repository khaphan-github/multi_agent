from agents import RunContextWrapper, function_tool
from ..models.models import CustomContexModel


@function_tool
async def get_tinh_huong(wrapper: RunContextWrapper[CustomContexModel]) -> str:
    return f"Mô tả tình huống là: {wrapper.context.mo_ta} "
