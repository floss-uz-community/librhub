from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep, pagination_dep
from app.db.session import get_db
from app.models.bookmarks import PostBookmark
from app.models.post import Post
from app.schemas.bookmark import BookmarkResponse

router = APIRouter()


@router.get("/", response_model=list[BookmarkResponse])
async def bookmarks_list(
    pagination: pagination_dep,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PostBookmark)
        .where(PostBookmark.user_id == current_user.id)
        .order_by(PostBookmark.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    return result.scalars().all()


@router.post(
    "/posts/{post_id}/",
    response_model=BookmarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def bookmark_create(
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    existing = await db.scalar(
        select(PostBookmark).where(
            PostBookmark.post_id == post_id,
            PostBookmark.user_id == current_user.id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post already bookmarked.",
        )

    bookmark = PostBookmark(post_id=post_id, user_id=current_user.id)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark


@router.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def bookmark_delete(
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(PostBookmark).where(
            PostBookmark.post_id == post_id,
            PostBookmark.user_id == current_user.id,
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
