from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.post import Post
from app.models.revisions import PostRevision
from app.schemas.revision import RevisionResponse

router = APIRouter()


@router.get("/post/{post_id}/", response_model=list[RevisionResponse])
async def revisions_by_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    result = await db.execute(
        select(PostRevision)
        .where(PostRevision.post_id == post_id)
        .order_by(PostRevision.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{revision_id}/", response_model=RevisionResponse)
async def revision_detail(revision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PostRevision).where(PostRevision.id == revision_id)
    )
    revision = result.scalar_one_or_none()
    if not revision:
        return JSONResponse(
            {"error": "Revision not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return revision
