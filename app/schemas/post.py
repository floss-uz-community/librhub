from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.enums import PostStatus


class PostCreate(BaseModel):
    category_id: int
    title: str
    slug: str | None = None
    excerpt: str | None = None
    body: str
    status: PostStatus = PostStatus.DRAFT
    published_at: datetime | None = None
    scheduled_at: datetime | None = None


class PostUpdate(BaseModel):
    category_id: int | None = None
    title: str | None = None
    slug: str | None = None
    excerpt: str | None = None
    body: str | None = None
    status: PostStatus | None = None
    published_at: datetime | None = None
    scheduled_at: datetime | None = None


class PostResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    title: str
    slug: str
    excerpt: str | None
    body: str
    views_count: int
    comments_count: int
    bookmarks_count: int
    score: int
    status: PostStatus
    published_at: datetime | None
    scheduled_at: datetime | None
    edited_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
