from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.db.session import get_db
from app.models.profession import Profession
from app.models.users import User
from app.core.security import (
    hash_password,
    generate_typed_token,
    decode_typed_token,
    send_email,
)
from app.core.limiter import limiter
from app.api.dependencies import current_user_jwt_dep, pagination_dep

router = APIRouter()


def _normalize_username(user_in: UserCreate) -> str:
    if user_in.username and user_in.username.strip():
        return user_in.username.strip().lower()
    return user_in.email.split("@")[0].strip().lower()


def _can_manage_target_user(current_user: User, target_user_id: int) -> bool:
    return current_user.is_superuser or current_user.id == target_user_id


@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
async def user_create(
    request: Request,
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    username = _normalize_username(user_in)
    profession_id = (
        None if user_in.profession_id in (None, 0) else user_in.profession_id
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
        is_staff=False,
        is_superuser=False,
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

    token = generate_typed_token(new_user.id, "email_verify", expire_minutes=24 * 60)
    background_tasks.add_task(
        send_email,
        new_user.email,
        "Verify your LibrHub email",
        f"Click the link to verify your email:\n\n"
        f"http://localhost:3000/verify-email?token={token}\n\n"
        f"This link expires in 24 hours.",
    )

    return new_user


@router.get("/verify-email")
async def verify_email(token: str = Query(...), db: AsyncSession = Depends(get_db)):
    user_id = decode_typed_token(token, "email_verify")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.email_verified_at is not None:
        return {"detail": "Email already verified."}

    user.email_verified_at = datetime.now(timezone.utc)
    await db.commit()
    return {"detail": "Email verified successfully."}


@router.get("/list", response_model=list[UserResponse])
async def users_list(
    pagination: pagination_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).offset(pagination.offset).limit(pagination.limit)
    )
    return result.scalars().all()


@router.get("/{user_id}/", response_model=UserResponse)
async def user_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.put("/{user_id}/", response_model=UserResponse)
async def user_update(
    user_id: int,
    user_in: UserUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    if not _can_manage_target_user(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    update_data = user_in.model_dump(exclude_unset=True)
    if (
        "is_staff" in update_data or "is_superuser" in update_data
    ) and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can change role flags.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}")
async def user_delete(
    user_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    if not _can_manage_target_user(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(user)
    await db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
