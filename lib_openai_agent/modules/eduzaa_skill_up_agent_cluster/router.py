# Viet router dieu huong vao service router goi provider
from typing import Optional
from fastapi import APIRouter, Header,  Request
from fastapi.responses import StreamingResponse
from .dto import ChatRequest
from .providers import service_manager

# Create rate limiter for API protection
router = APIRouter(prefix="/skill-up", tags=["skill-up"])


@router.post("/chat")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    x_contactid: Optional[str] = Header(None, alias="x-contactid"),
):
    stream_generator = await service_manager.run(
        user_id=x_contactid,
        chat_id=chat_request.chat_id,
        skill_id=chat_request.skill_id,
        message=chat_request.message
    )

    return StreamingResponse(
        stream_generator,
        media_type="text/event-stream"
    )
