from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    thread_id: str
    status: str
    message: str | None = None
    approval: dict[str, Any] | None = None


class ApprovalRequest(BaseModel):
    thread_id: str = Field(min_length=1, max_length=100)
    approval_id: str = Field(min_length=1, max_length=64)
    approved: bool


class ApprovalResponse(BaseModel):
    thread_id: str
    status: str
    message: str