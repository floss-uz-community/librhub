from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MediaCreate(BaseModel):
    url: str
    mime_type: str | None = None
    alt_text: str | None = None


class MediaUpdate(BaseModel):
    url: str | None = None
    mime_type: str | None = None
    alt_text: str | None = None


class MediaResponse(BaseModel):
    id: int
    url: str
    mime_type: str | None
    alt_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostMediaResponse(BaseModel):
    id: int
    post_id: int
    media_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
