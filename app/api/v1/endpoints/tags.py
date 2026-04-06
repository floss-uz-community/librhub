from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep
from app.core.security import generate_slug
from app.db.session import get_db
from app.models.tags import Tag
from app.models.post_tag import PostTag
from app.models.post import Post
from app.models.users import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate

router = APIRouter()


def _require_staff(user: User) -> None:
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required.",
        )


def _normalize_tag_slug(name: str, slug: str | None) -> str:
    if slug and slug.strip():
        return generate_slug(slug.strip())
    return generate_slug(name.strip())


@router.get("/", response_model=list[TagResponse])
async def tags_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.name))
    return result.scalars().all()


@router.get("/{tag_id}/", response_model=TagResponse)
async def tag_detail(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        return JSONResponse(
            {"error": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def tag_create(
    body: TagCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    slug = _normalize_tag_slug(body.name, body.slug)
    existing = await db.scalar(select(Tag).where(Tag.slug == slug))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag slug already exists.",
        )

    tag = Tag(name=body.name, slug=slug)

    try:
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already exists.",
        )

    return tag


@router.put("/{tag_id}/", response_model=TagResponse)
async def tag_update(
    tag_id: int,
    body: TagUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        return JSONResponse(
            {"error": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    update_data = body.model_dump(exclude_unset=True)

    if "name" in update_data or "slug" in update_data:
        name_for_slug = update_data.get("name", tag.name)
        provided_slug = update_data.get("slug")
        new_slug = _normalize_tag_slug(name_for_slug, provided_slug)

        existing = await db.scalar(
            select(Tag).where(Tag.slug == new_slug, Tag.id != tag.id)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tag slug already exists.",
            )
        update_data["slug"] = new_slug

    for field, value in update_data.items():
        setattr(tag, field, value)

    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@router.delete("/{tag_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def tag_delete(
    tag_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        return JSONResponse(
            {"error": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(tag)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{tag_id}/posts/{post_id}/",
    status_code=status.HTTP_201_CREATED,
)
async def tag_add_to_post(
    tag_id: int,
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    tag = await db.scalar(select(Tag).where(Tag.id == tag_id))
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )

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

    existing = await db.scalar(
        select(PostTag).where(PostTag.post_id == post_id, PostTag.tag_id == tag_id)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already assigned to this post.",
        )

    db.add(PostTag(post_id=post_id, tag_id=tag_id))
    await db.commit()
    return {"detail": "Tag added to post."}


@router.delete("/{tag_id}/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def tag_remove_from_post(
    tag_id: int,
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
        select(PostTag).where(PostTag.post_id == post_id, PostTag.tag_id == tag_id)
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag is not assigned to this post.",
        )

    await db.delete(link)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
