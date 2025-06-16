# VIET CAC DTO Nhan request

from typing import Any, Dict, Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    skill_id: str
