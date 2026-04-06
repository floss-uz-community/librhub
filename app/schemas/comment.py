from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import CommentStatus


class CommentCreate(BaseModel):
    post_id: int
    parent_id: int | None = None
    text: str


class CommentUpdate(BaseModel):
    text: str | None = None
    status: CommentStatus | None = None


class CommentResponse(BaseModel):
    id: int
    user_id: int | None
    post_id: int
    parent_id: int | None
    text: str
    status: CommentStatus
    score: int
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
