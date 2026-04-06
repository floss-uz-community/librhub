from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep
from app.core.security import generate_slug
from app.db.session import get_db
from app.models.category import Category
from app.models.users import User
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter()


def _require_staff(user: User) -> None:
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required.",
        )


def _normalize_category_slug(name: str, slug: str | None) -> str:
    if slug and slug.strip():
        return generate_slug(slug.strip())
    return generate_slug(name.strip())


@router.get("/", response_model=list[CategoryResponse])
async def categories_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.name))
    return result.scalars().all()


@router.get("/{category_id}/", response_model=CategoryResponse)
async def category_detail(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        return JSONResponse(
            {"error": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return category


@router.post(
    "/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def category_create(
    body: CategoryCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    slug = _normalize_category_slug(body.name, body.slug)
    existing = await db.scalar(select(Category).where(Category.slug == slug))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category slug already exists.",
        )

    category = Category(name=body.name, slug=slug)

    try:
        db.add(category)
        await db.commit()
        await db.refresh(category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists.",
        )

    return category


@router.put("/{category_id}/", response_model=CategoryResponse)
async def category_update(
    category_id: int,
    body: CategoryUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        return JSONResponse(
            {"error": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    update_data = body.model_dump(exclude_unset=True)

    if "name" in update_data or "slug" in update_data:
        name_for_slug = update_data.get("name", category.name)
        provided_slug = update_data.get("slug")
        new_slug = _normalize_category_slug(name_for_slug, provided_slug)

        existing = await db.scalar(
            select(Category).where(Category.slug == new_slug, Category.id != category.id)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category slug already exists.",
            )
        update_data["slug"] = new_slug

    for field, value in update_data.items():
        setattr(category, field, value)

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def category_delete(
    category_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        return JSONResponse(
            {"error": "Category not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(category)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
