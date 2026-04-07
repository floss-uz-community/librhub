from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookmarkResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
