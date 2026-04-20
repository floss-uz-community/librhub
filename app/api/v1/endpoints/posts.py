from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import current_user_jwt_dep, pagination_dep
from app.core.security import generate_slug
from app.db.session import get_db
from app.models.category import Category
from app.models.enums import PostStatus
from app.models.post import Post
from app.models.post_tag import PostTag
from app.models.revisions import PostRevision
from app.models.users import User
from app.models.votes import PostVote
from app.schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter()


def _post_options():
    return [selectinload(Post.author), selectinload(Post.category)]


def _can_manage_target_post(current_user: User, post: Post) -> bool:
    return current_user.is_superuser or current_user.id == post.user_id


def _normalize_post_slug(title: str, slug: str | None) -> str:
    if slug and slug.strip():
        return generate_slug(slug.strip())
    return generate_slug(title.strip())


async def _validate_category_exists(db: AsyncSession, category_id: int) -> None:
    category_exists = await db.scalar(
        select(Category.id).where(Category.id == category_id)
    )
    if not category_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid category_id.",
        )


def _validate_schedule_fields(
    post_status: PostStatus | None,
    scheduled_at: datetime | None,
) -> None:
    if post_status == PostStatus.SCHEDULED and scheduled_at is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="scheduled_at is required when status is scheduled.",
        )


@router.get("/", response_model=list[PostResponse])
async def posts_list(
    pagination: pagination_dep,
    status_filter: PostStatus | None = Query(None, alias="status"),
    category_id: int | None = None,
    tag_id: int | None = None,
    q: str | None = Query(None, description="Search in title and body"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Post).options(*_post_options())

    if status_filter is not None:
        stmt = stmt.where(Post.status == status_filter)
    if category_id is not None:
        stmt = stmt.where(Post.category_id == category_id)
    if tag_id is not None:
        stmt = stmt.join(PostTag, PostTag.post_id == Post.id).where(
            PostTag.tag_id == tag_id
        )
    if q:
        term = f"%{q}%"
        stmt = stmt.where(Post.title.ilike(term) | Post.body.ilike(term))

    stmt = stmt.order_by(Post.created_at.desc()).offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/trending", response_model=list[PostResponse])
async def posts_trending(
    pagination: pagination_dep,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Post)
        .options(*_post_options())
        .outerjoin(PostVote, PostVote.post_id == Post.id)
        .group_by(Post.id)
        .order_by(func.count(PostVote.id).desc(), Post.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{post_id}/", response_model=PostResponse)
async def post_detail(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).options(*_post_options()).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    await db.execute(
        update(Post).where(Post.id == post_id).values(views_count=Post.views_count + 1)
    )
    await db.commit()
    await db.refresh(post)
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def post_create(
    post_in: PostCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    await _validate_category_exists(db, post_in.category_id)
    _validate_schedule_fields(post_in.status, post_in.scheduled_at)

    normalized_slug = _normalize_post_slug(post_in.title, post_in.slug)
    existing_post_by_slug = await db.scalar(
        select(Post).where(Post.slug == normalized_slug)
    )
    if existing_post_by_slug:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug already exists.",
        )

    published_at = post_in.published_at
    if post_in.status == PostStatus.PUBLISHED and published_at is None:
        published_at = datetime.now(timezone.utc)

    new_post = Post(
        user_id=current_user.id,
        category_id=post_in.category_id,
        title=post_in.title,
        slug=normalized_slug,
        excerpt=post_in.excerpt,
        body=post_in.body,
        status=post_in.status,
        published_at=published_at,
        scheduled_at=post_in.scheduled_at,
    )

    try:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post with provided data already exists.",
        )

    result = await db.execute(
        select(Post).options(*_post_options()).where(Post.id == new_post.id)
    )
    return result.scalar_one()


@router.put("/{post_id}/", response_model=PostResponse)
async def post_update(
    post_id: int,
    post_in: PostUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    if not _can_manage_target_post(current_user, post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    update_data = post_in.model_dump(exclude_unset=True)
    new_category_id = update_data.get("category_id")
    if new_category_id is not None:
        await _validate_category_exists(db, new_category_id)

    new_status = update_data.get("status", post.status)
    new_scheduled_at = update_data.get("scheduled_at", post.scheduled_at)
    _validate_schedule_fields(new_status, new_scheduled_at)

    if "title" in update_data or "slug" in update_data:
        title_for_slug = update_data.get("title", post.title)
        provided_slug = update_data.get("slug")
        normalized_slug = _normalize_post_slug(title_for_slug, provided_slug)
        existing_post_by_slug = await db.scalar(
            select(Post).where(Post.slug == normalized_slug, Post.id != post.id)
        )
        if existing_post_by_slug:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Slug already exists.",
            )
        update_data["slug"] = normalized_slug

    if new_status == PostStatus.PUBLISHED and "published_at" not in update_data:
        update_data["published_at"] = datetime.now(timezone.utc)

    update_data["edited_at"] = datetime.now(timezone.utc)

    if "title" in update_data or "body" in update_data:
        revision = PostRevision(
            post_id=post.id,
            editor_user_id=current_user.id,
            title=post.title,
            body=post.body,
        )
        db.add(revision)

    for field, value in update_data.items():
        setattr(post, field, value)

    db.add(post)
    await db.commit()

    result = await db.execute(
        select(Post).options(*_post_options()).where(Post.id == post.id)
    )
    return result.scalar_one()


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    if not _can_manage_target_post(current_user, post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    await db.delete(post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
