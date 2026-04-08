from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep, pagination_dep
from app.db.session import get_db
from app.models.media import Media
from app.models.post import Post
from app.models.post_media import PostMedia
from app.models.users import User
from app.schemas.media import (
    MediaCreate,
    MediaResponse,
    MediaUpdate,
    PostMediaResponse,
)

router = APIRouter()


def _require_staff(user: User) -> None:
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required.",
        )


@router.get("/", response_model=list[MediaResponse])
async def media_list(
    pagination: pagination_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Media)
        .order_by(Media.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    return result.scalars().all()


@router.get("/{media_id}/", response_model=MediaResponse)
async def media_detail(media_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        return JSONResponse(
            {"error": "Media not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return media


@router.post("/", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def media_create(
    body: MediaCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    media = Media(url=body.url, mime_type=body.mime_type, alt_text=body.alt_text)
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


@router.put("/{media_id}/", response_model=MediaResponse)
async def media_update(
    media_id: int,
    body: MediaUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        return JSONResponse(
            {"error": "Media not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(media, field, value)

    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


@router.delete("/{media_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def media_delete(
    media_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        return JSONResponse(
            {"error": "Media not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(media)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ── Post-Media attachment ─────────────────────────────────────

@router.get("/post/{post_id}/", response_model=list[MediaResponse])
async def media_by_post(
    post_id: int,
    pagination: pagination_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    result = await db.execute(
        select(Media)
        .join(PostMedia, PostMedia.media_id == Media.id)
        .where(PostMedia.post_id == post_id)
        .order_by(PostMedia.created_at)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    return result.scalars().all()


@router.post(
    "/{media_id}/posts/{post_id}/",
    response_model=PostMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def media_attach_to_post(
    media_id: int,
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    if not (current_user.is_superuser or current_user.id == post.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    media = await db.scalar(select(Media).where(Media.id == media_id))
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found."
        )

    existing = await db.scalar(
        select(PostMedia).where(
            PostMedia.post_id == post_id, PostMedia.media_id == media_id
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Media already attached to this post.",
        )

    link = PostMedia(post_id=post_id, media_id=media_id)
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


@router.delete(
    "/{media_id}/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def media_detach_from_post(
    media_id: int,
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    if not (current_user.is_superuser or current_user.id == post.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    link = await db.scalar(
        select(PostMedia).where(
            PostMedia.post_id == post_id, PostMedia.media_id == media_id
        )
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media is not attached to this post.",
        )

    await db.delete(link)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
