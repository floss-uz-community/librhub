from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep, pagination_dep
from app.db.session import get_db
from app.models.profession import Profession
from app.models.users import User
from app.schemas.profession import ProfessionCreate, ProfessionResponse, ProfessionUpdate

router = APIRouter()


def _require_staff(user: User) -> None:
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required.",
        )


@router.get("/", response_model=list[ProfessionResponse])
async def professions_list(
    pagination: pagination_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profession).order_by(Profession.name).offset(pagination.offset).limit(pagination.limit)
    )
    return result.scalars().all()


@router.get("/{profession_id}/", response_model=ProfessionResponse)
async def profession_detail(profession_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Profession).where(Profession.id == profession_id)
    )
    profession = result.scalar_one_or_none()
    if not profession:
        return JSONResponse(
            {"error": "Profession not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return profession


@router.post(
    "/", response_model=ProfessionResponse, status_code=status.HTTP_201_CREATED
)
async def profession_create(
    body: ProfessionCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    profession = Profession(name=body.name)

    try:
        db.add(profession)
        await db.commit()
        await db.refresh(profession)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profession already exists.",
        )

    return profession


@router.put("/{profession_id}/", response_model=ProfessionResponse)
async def profession_update(
    profession_id: int,
    body: ProfessionUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(
        select(Profession).where(Profession.id == profession_id)
    )
    profession = result.scalar_one_or_none()
    if not profession:
        return JSONResponse(
            {"error": "Profession not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profession, field, value)

    try:
        db.add(profession)
        await db.commit()
        await db.refresh(profession)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profession name already exists.",
        )

    return profession


@router.delete("/{profession_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def profession_delete(
    profession_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    _require_staff(current_user)

    result = await db.execute(
        select(Profession).where(Profession.id == profession_id)
    )
    profession = result.scalar_one_or_none()
    if not profession:
        return JSONResponse(
            {"error": "Profession not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(profession)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
