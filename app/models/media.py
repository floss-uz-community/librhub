from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(255), nullable=True)

    post_media: Mapped[list["PostMedia"]] = relationship(
        "PostMedia", back_populates="media"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="media")
