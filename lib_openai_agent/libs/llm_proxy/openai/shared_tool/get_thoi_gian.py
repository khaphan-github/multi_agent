from datetime import datetime
import pytz
from ..openai_tool import OpenAIFunctionCall
from config.main import config


async def get_thoi_gian() -> str:
    try:
        tz = pytz.timezone(config.TZ)
        current_time = datetime.now(tz).isoformat()
        return current_time
    except pytz.UnknownTimeZoneError as e:
        print(f"Error: {e}")
        return None


OPEN_AI_GET_THOI_GIAN_TOOL = OpenAIFunctionCall(
    get_thoi_gian
)
