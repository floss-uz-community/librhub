from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(25), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(25), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(String(500), default="")
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    profession_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("profession.id", ondelete="SET NULL"), nullable=True
    )

    posts_count: Mapped[int] = mapped_column(BigInteger, default=0)
    posts_read_count: Mapped[int] = mapped_column(BigInteger, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="users"
    )
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    user_sessions: Mapped[list["UserSessionToken"]] = relationship(
        "UserSessionToken", back_populates="user"
    )
    post_votes: Mapped[list["PostVote"]] = relationship(
        "PostVote", back_populates="user"
    )
    comment_votes: Mapped[list["CommentVote"]] = relationship(
        "CommentVote", back_populates="user"
    )
    bookmarks: Mapped[list["PostBookmark"]] = relationship(
        "PostBookmark", back_populates="user"
    )
    followers: Mapped[list["UserFollow"]] = relationship(
        "UserFollow", foreign_keys="UserFollow.followed_user_id", back_populates="followed_user"
    )
    following: Mapped[list["UserFollow"]] = relationship(
        "UserFollow", foreign_keys="UserFollow.follower_user_id", back_populates="follower_user"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", foreign_keys="Notification.recipient_user_id", back_populates="recipient"
    )
    sent_notifications: Mapped[list["Notification"]] = relationship(
        "Notification", foreign_keys="Notification.actor_user_id", back_populates="actor"
    )
    reports: Mapped[list["ModerationReport"]] = relationship(
        "ModerationReport", foreign_keys="ModerationReport.reporter_user_id", back_populates="reporter"
    )
    moderation_actions: Mapped[list["ModerationAction"]] = relationship(
        "ModerationAction", foreign_keys="ModerationAction.moderator_user_id", back_populates="moderator"
    )
