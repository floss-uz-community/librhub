from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.models.enums import CommentStatus


class Comment(BaseModel):
    __tablename__ = "comment"
    __table_args__ = (
        Index("ix_comment_post_id", "post_id"),
        Index("ix_comment_user_id", "user_id"),
        Index("ix_comment_parent_id", "parent_id"),
        Index("ix_comment_status", "status"),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    media_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("media.id", ondelete="SET NULL"), nullable=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("comment.id", ondelete="CASCADE"), nullable=True
    )

    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CommentStatus] = mapped_column(
        Enum(CommentStatus, name="comment_status"),
        default=CommentStatus.VISIBLE,
        nullable=False,
    )
    score: Mapped[int] = mapped_column(default=0)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    media: Mapped["Media | None"] = relationship("Media", back_populates="comments")
    parent: Mapped["Comment | None"] = relationship(
        "Comment", remote_side="Comment.id", back_populates="children"
    )
    children: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="parent", cascade="all, delete-orphan"
    )
    votes: Mapped[list["CommentVote"]] = relationship(
        "CommentVote", back_populates="comment"
    )
