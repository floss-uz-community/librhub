from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import pagination_dep
from app.db.session import get_db
from app.models.enums import PostStatus
from app.models.post import Post
from app.models.tags import Tag
from app.models.users import User
from app.schemas.post import PostResponse
from app.schemas.tag import TagResponse
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/posts", response_model=list[PostResponse])
async def search_posts(
    q: str = Query(..., min_length=1, description="Search query"),
    pagination: pagination_dep = ...,
    db: AsyncSession = Depends(get_db),
):
    term = f"%{q}%"
    stmt = (
        select(Post)
        .options(selectinload(Post.author), selectinload(Post.category))
        .where(
            Post.status == PostStatus.PUBLISHED,
            or_(
                Post.title.ilike(term),
                Post.excerpt.ilike(term),
                Post.body.ilike(term),
            ),
        )
        .order_by(Post.published_at.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/users", response_model=list[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1, description="Search query"),
    pagination: pagination_dep = ...,
    db: AsyncSession = Depends(get_db),
):
    term = f"%{q}%"
    stmt = (
        select(User)
        .where(
            User.is_active == True,
            User.is_deleted == False,
            or_(
                User.username.ilike(term),
                User.display_name.ilike(term),
                User.first_name.ilike(term),
                User.last_name.ilike(term),
            ),
        )
        .order_by(User.username)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/tags", response_model=list[TagResponse])
async def search_tags(
    q: str = Query(..., min_length=1, description="Search query"),
    pagination: pagination_dep = ...,
    db: AsyncSession = Depends(get_db),
):
    term = f"%{q}%"
    stmt = (
        select(Tag)
        .where(Tag.name.ilike(term))
        .order_by(Tag.name)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
