
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field


@dataclass
class CustomContexModel:
    mo_ta: str
    history: List[str] = Field(
        default_factory=list,
        description="Lịch sử trò chuyện của người dùng, bao gồm các câu hỏi và phản hồi trước đó",
    )
    # Thong tin nguoi dung


class UserMetadata(BaseModel):
    user_id: str = '1937'
    hitory: List[str] = Field(
        default_factory=list,
        description="Lịch sử trò chuyện của người dùng, bao gồm các câu hỏi và phản hồi trước đó",
    )


class HintAgentOutput(BaseModel):
    hint: Optional[List[str]] = Field(
        description="Ý tưởng gợi ý chung chung để người dùng có hướng suy nghĩ - co the co hoac khong co neu co message thi khong hien thi truong nay",
    )


class GenerateResponseAgentOutput(BaseModel):
    type_result: str = Field(
        description='''
        Dinh dang ket qua tra ve ung voi tung nghiep vu cu the
        - hint: Kết quả từ Agent Gợi ý
        - solution: Kết quả từ Agent Giải pháp Hệ thống
        - clarification: Kết quả từ Agent Làm rõ tình huống
        - direct_answer: Kết quả từ Agent trả lời trực tiếp câu hỏi đơn giản
        - other: Kết quả từ Agent khác không thuộc các loại trên
        '''
    )
    response: str | List[str] = Field(
        description="Phản hồi cuối cùng cho người dùng",
    )
