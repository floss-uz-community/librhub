from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RevisionResponse(BaseModel):
    id: int
    post_id: int
    editor_user_id: int | None
    title: str
    body: str
    change_summary: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
