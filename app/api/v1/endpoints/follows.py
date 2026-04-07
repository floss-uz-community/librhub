from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep
from app.db.session import get_db
from app.models.category import Category
from app.models.follows import CategoryFollow, TagFollow, UserFollow
from app.models.tags import Tag
from app.models.users import User
from app.schemas.follow import (
    CategoryFollowResponse,
    TagFollowResponse,
    UserFollowResponse,
)

router = APIRouter()


# ── User follows ──────────────────────────────────────────────

@router.get("/users/", response_model=list[UserFollowResponse])
async def user_following_list(
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserFollow)
        .where(UserFollow.follower_user_id == current_user.id)
        .order_by(UserFollow.created_at.desc())
    )
    return result.scalars().all()


@router.post(
    "/users/{user_id}/",
    response_model=UserFollowResponse,
    status_code=status.HTTP_201_CREATED,
)
async def user_follow_create(
    user_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself.",
        )

    target = await db.scalar(select(User).where(User.id == user_id))
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    existing = await db.scalar(
        select(UserFollow).where(
            UserFollow.follower_user_id == current_user.id,
            UserFollow.followed_user_id == user_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already following this user.",
        )

    follow = UserFollow(follower_user_id=current_user.id, followed_user_id=user_id)
    db.add(follow)
    await db.commit()
    await db.refresh(follow)
    return follow


@router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def user_follow_delete(
    user_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(UserFollow).where(
            UserFollow.follower_user_id == current_user.id,
            UserFollow.followed_user_id == user_id,
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ── Tag follows ───────────────────────────────────────────────

@router.get("/tags/", response_model=list[TagFollowResponse])
async def tag_following_list(
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TagFollow)
        .where(TagFollow.user_id == current_user.id)
        .order_by(TagFollow.created_at.desc())
    )
    return result.scalars().all()


@router.post(
    "/tags/{tag_id}/",
    response_model=TagFollowResponse,
    status_code=status.HTTP_201_CREATED,
)
async def tag_follow_create(
    tag_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    tag = await db.scalar(select(Tag).where(Tag.id == tag_id))
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )

    existing = await db.scalar(
        select(TagFollow).where(
            TagFollow.user_id == current_user.id,
            TagFollow.tag_id == tag_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already following this tag.",
        )

    follow = TagFollow(user_id=current_user.id, tag_id=tag_id)
    db.add(follow)
    await db.commit()
    await db.refresh(follow)
    return follow


@router.delete("/tags/{tag_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def tag_follow_delete(
    tag_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(TagFollow).where(
            TagFollow.user_id == current_user.id,
            TagFollow.tag_id == tag_id,
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ── Category follows ─────────────────────────────────────────

@router.get("/categories/", response_model=list[CategoryFollowResponse])
async def category_following_list(
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CategoryFollow)
        .where(CategoryFollow.user_id == current_user.id)
        .order_by(CategoryFollow.created_at.desc())
    )
    return result.scalars().all()


@router.post(
    "/categories/{category_id}/",
    response_model=CategoryFollowResponse,
    status_code=status.HTTP_201_CREATED,
)
async def category_follow_create(
    category_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    category = await db.scalar(select(Category).where(Category.id == category_id))
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )

    existing = await db.scalar(
        select(CategoryFollow).where(
            CategoryFollow.user_id == current_user.id,
            CategoryFollow.category_id == category_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already following this category.",
        )

    follow = CategoryFollow(user_id=current_user.id, category_id=category_id)
    db.add(follow)
    await db.commit()
    await db.refresh(follow)
    return follow


@router.delete("/categories/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def category_follow_delete(
    category_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(CategoryFollow).where(
            CategoryFollow.user_id == current_user.id,
            CategoryFollow.category_id == category_id,
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
