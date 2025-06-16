from datetime import datetime
import pytz
from agents.tool import function_tool


@function_tool
def get_current_time() -> str:
    """Get the current date and time.

    Returns:
        A string containing the current date and time in Asia/Ho_Chi_Minh timezone.
    """
    hcm_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(hcm_timezone)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
