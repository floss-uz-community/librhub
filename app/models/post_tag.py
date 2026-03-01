from sqlalchemy import BigInteger, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class PostTag(BaseModel):
    __tablename__ = "post_tag"
    __table_args__ = (
        UniqueConstraint("post_id", "tag_id", name="uq_post_tag_post_id_tag_id"),
        Index("ix_post_tag_post_id", "post_id"),
        Index("ix_post_tag_tag_id", "tag_id"),
    )

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="posts")
