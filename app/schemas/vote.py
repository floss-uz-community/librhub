from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class VoteCreate(BaseModel):
    value: Literal[-1, 1]


class PostVoteResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    value: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentVoteResponse(BaseModel):
    id: int
    comment_id: int
    user_id: int
    value: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
