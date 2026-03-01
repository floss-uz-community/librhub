from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import NotificationType


class Notification(BaseModel):
    __tablename__ = "notification"
    __table_args__ = (
        Index("ix_notification_recipient_user_id", "recipient_user_id"),
        Index("ix_notification_actor_user_id", "actor_user_id"),
        Index("ix_notification_is_read", "is_read"),
        Index("ix_notification_type", "type"),
    )

    recipient_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    actor_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type"), nullable=False
    )
    payload: Mapped[str] = mapped_column(String(2000), nullable=False, default="{}")
    is_read: Mapped[bool] = mapped_column(default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    recipient: Mapped["User"] = relationship(
        "User",
        foreign_keys=[recipient_user_id],
        back_populates="notifications",
    )
    actor: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[actor_user_id],
        back_populates="sent_notifications",
    )
