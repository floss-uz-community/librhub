from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    verify_password,
    generate_jwt_tokens,
    decode_jwt_token,
    generate_typed_token,
    decode_typed_token,
    hash_password,
    send_email,
)
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.users import User
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    AccessTokenResponse,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active or user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive or deleted.",
        )

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    access_token, refresh_token = generate_jwt_tokens(user.id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    decoded = decode_jwt_token(body.refresh_token)
    raw_user_id = decoded.get("sub")
    if raw_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active or user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive.",
        )

    access_token = generate_jwt_tokens(user.id, is_access_only=True)

    return AccessTokenResponse(access_token=access_token)


@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    body: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    # Always return 200 to avoid email enumeration
    if user and user.is_active and not user.is_deleted:
        token = generate_typed_token(user.id, "password_reset", expire_minutes=60)
        background_tasks.add_task(
            send_email,
            user.email,
            "Reset your LibrHub password",
            f"Click the link to reset your password:\n\n"
            f"http://localhost:3000/reset-password?token={token}\n\n"
            f"This link expires in 1 hour. If you didn't request this, ignore this email.",
        )

    return {"detail": "If that email exists, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    user_id = decode_typed_token(body.token, "password_reset")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active or user.is_deleted:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    user.password_hash = hash_password(body.new_password)
    await db.commit()
    return {"detail": "Password reset successfully."}
