from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.models.enums import PostStatus


class Post(BaseModel):
    __tablename__ = "post"
    __table_args__ = (
        Index("ix_post_user_id", "user_id"),
        Index("ix_post_category_id", "category_id"),
        Index("ix_post_status", "status"),
        Index("ix_post_published_at", "published_at"),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("category.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    bookmarks_count: Mapped[int] = mapped_column(BigInteger, default=0)
    score: Mapped[int] = mapped_column(default=0)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, name="post_status"), default=PostStatus.DRAFT, nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    edited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[list["PostMedia"]] = relationship("PostMedia", back_populates="post")
    tags: Mapped[list["PostTag"]] = relationship("PostTag", back_populates="post")
    revisions: Mapped[list["PostRevision"]] = relationship(
        "PostRevision", back_populates="post"
    )
    votes: Mapped[list["PostVote"]] = relationship("PostVote", back_populates="post")
    bookmarks: Mapped[list["PostBookmark"]] = relationship(
        "PostBookmark", back_populates="post"
    )
