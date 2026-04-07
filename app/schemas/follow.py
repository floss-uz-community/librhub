from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserFollowResponse(BaseModel):
    id: int
    follower_user_id: int
    followed_user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagFollowResponse(BaseModel):
    id: int
    user_id: int
    tag_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryFollowResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
