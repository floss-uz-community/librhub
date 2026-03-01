from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Index,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class PostVote(BaseModel):
    __tablename__ = "post_vote"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_post_vote_post_id_user_id"),
        CheckConstraint("value IN (-1, 1)", name="ck_post_vote_value"),
        Index("ix_post_vote_post_id", "post_id"),
        Index("ix_post_vote_user_id", "user_id"),
    )

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="votes")
    user: Mapped["User"] = relationship("User", back_populates="post_votes")


class CommentVote(BaseModel):
    __tablename__ = "comment_vote"
    __table_args__ = (
        UniqueConstraint(
            "comment_id", "user_id", name="uq_comment_vote_comment_id_user_id"
        ),
        CheckConstraint("value IN (-1, 1)", name="ck_comment_vote_value"),
        Index("ix_comment_vote_comment_id", "comment_id"),
        Index("ix_comment_vote_user_id", "user_id"),
    )

    comment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("comment.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    comment: Mapped["Comment"] = relationship("Comment", back_populates="votes")
    user: Mapped["User"] = relationship("User", back_populates="comment_votes")

