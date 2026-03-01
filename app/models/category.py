from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")
    followers: Mapped[list["CategoryFollow"]] = relationship(
        "CategoryFollow", back_populates="category"
    )
