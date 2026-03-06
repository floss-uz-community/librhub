from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db
from app.models.profession import Profession
from app.models.users import User
from app.core.security import hash_password

router = APIRouter()


def _normalize_username(user_in: UserCreate) -> str:
    if user_in.username and user_in.username.strip():
        return user_in.username.strip().lower()
    return user_in.email.split("@")[0].strip().lower()


@router.post("/register", response_model=UserResponse)
async def user_create(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    username = _normalize_username(user_in)
    profession_id = (
        None
        if user_in.profession_id in (None, 0)
        else user_in.profession_id
    )

    existing_user_by_email = await db.scalar(
        select(User).where(User.email == user_in.email)
    )
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    existing_user_by_username = await db.scalar(
        select(User).where(User.username == username)
    )
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    if profession_id is not None:
        profession_exists = await db.scalar(
            select(Profession.id).where(Profession.id == profession_id)
        )
        if not profession_exists:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid profession_id.",
            )

    new_user = User(
        username=username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        bio=user_in.bio or "",
        profession_id=profession_id,
        is_active=user_in.is_active,
        is_staff=user_in.is_staff,
        is_superuser=user_in.is_superuser,
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with provided credentials already exists.",
        )

    return new_user
