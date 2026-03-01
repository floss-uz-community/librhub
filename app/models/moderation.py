from sqlalchemy import BigInteger, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import ModerationActionType, ModerationTargetType


class ModerationReport(BaseModel):
    __tablename__ = "moderation_report"
    __table_args__ = (
        Index("ix_moderation_report_reporter_user_id", "reporter_user_id"),
        Index("ix_moderation_report_target_type_target_id", "target_type", "target_id"),
        Index("ix_moderation_report_status", "status"),
    )

    reporter_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    target_type: Mapped[ModerationTargetType] = mapped_column(
        Enum(ModerationTargetType, name="moderation_target_type"), nullable=False
    )
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    reporter: Mapped["User"] = relationship(
        "User", foreign_keys=[reporter_user_id], back_populates="reports"
    )
    actions: Mapped[list["ModerationAction"]] = relationship(
        "ModerationAction", back_populates="report"
    )


class ModerationAction(BaseModel):
    __tablename__ = "moderation_action"
    __table_args__ = (
        Index("ix_moderation_action_report_id", "report_id"),
        Index("ix_moderation_action_moderator_user_id", "moderator_user_id"),
    )

    report_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("moderation_report.id", ondelete="CASCADE"), nullable=False
    )
    moderator_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    action_type: Mapped[ModerationActionType] = mapped_column(
        Enum(ModerationActionType, name="moderation_action_type"), nullable=False
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    report: Mapped["ModerationReport"] = relationship(
        "ModerationReport", back_populates="actions"
    )
    moderator: Mapped["User | None"] = relationship(
        "User", foreign_keys=[moderator_user_id], back_populates="moderation_actions"
    )

