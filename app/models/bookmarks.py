from sqlalchemy import BigInteger, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class PostBookmark(BaseModel):
    __tablename__ = "post_bookmark"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_post_bookmark_post_id_user_id"),
        Index("ix_post_bookmark_post_id", "post_id"),
        Index("ix_post_bookmark_user_id", "user_id"),
    )

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="bookmarks")
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")

