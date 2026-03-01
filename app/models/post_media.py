from sqlalchemy import BigInteger, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class PostMedia(BaseModel):
    __tablename__ = "post_media"
    __table_args__ = (
        UniqueConstraint("post_id", "media_id", name="uq_post_media_post_id_media_id"),
        Index("ix_post_media_post_id", "post_id"),
        Index("ix_post_media_media_id", "media_id"),
    )

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    media_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("media.id", ondelete="CASCADE"), nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="media")
    media: Mapped["Media"] = relationship("Media", back_populates="post_media")
