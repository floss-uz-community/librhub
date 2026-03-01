from sqlalchemy import BigInteger, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class UserFollow(BaseModel):
    __tablename__ = "user_follow"
    __table_args__ = (
        UniqueConstraint(
            "follower_user_id",
            "followed_user_id",
            name="uq_user_follow_follower_followed",
        ),
        Index("ix_user_follow_follower_user_id", "follower_user_id"),
        Index("ix_user_follow_followed_user_id", "followed_user_id"),
    )

    follower_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    followed_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    follower_user: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_user_id], back_populates="following"
    )
    followed_user: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_user_id], back_populates="followers"
    )


class TagFollow(BaseModel):
    __tablename__ = "tag_follow"
    __table_args__ = (
        UniqueConstraint("user_id", "tag_id", name="uq_tag_follow_user_id_tag_id"),
        Index("ix_tag_follow_user_id", "user_id"),
        Index("ix_tag_follow_tag_id", "tag_id"),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="followers")


class CategoryFollow(BaseModel):
    __tablename__ = "category_follow"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "category_id", name="uq_category_follow_user_id_category_id"
        ),
        Index("ix_category_follow_user_id", "user_id"),
        Index("ix_category_follow_category_id", "category_id"),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User")
    category: Mapped["Category"] = relationship("Category", back_populates="followers")

