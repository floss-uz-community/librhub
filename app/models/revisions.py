from sqlalchemy import BigInteger, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class PostRevision(BaseModel):
    __tablename__ = "post_revision"
    __table_args__ = (
        Index("ix_post_revision_post_id", "post_id"),
        Index("ix_post_revision_editor_user_id", "editor_user_id"),
    )

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    editor_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    change_summary: Mapped[str | None] = mapped_column(nullable=True)

    post: Mapped["Post"] = relationship("Post", back_populates="revisions")
    editor: Mapped["User | None"] = relationship("User")

