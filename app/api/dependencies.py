from typing import Annotated
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db as db_dep
from app.models import User, UserSessionToken
from app.core.security import verify_password, decode_jwt_token
from app.core.config import settings


basic = HTTPBasic()

jwt_security = HTTPBearer(auto_error=False)


async def get_current_user(
    session: AsyncSession = Depends(db_dep),
    credentials: HTTPBasicCredentials = Depends(basic),
):
    stmt = (
        select(User)
        .where(User.email == credentials.username)
        .options(joinedload(User.profession))
    )
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


current_user_basic_dep = Annotated[User, Depends(get_current_user)]


async def get_current_user_session(
    request: Request, session: AsyncSession = Depends(db_dep)
):
    sessionId = request.cookies.get("session_id")
    if not sessionId:
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = select(UserSessionToken).where(UserSessionToken.token == sessionId)
    result = await session.execute(stmt)
    session_obj = result.scalars().first()

    if not session_obj:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session_obj.expires_at < datetime.now(tz=timezone.utc):
        await session.delete(session_obj)
        await session.commit()
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = (
        select(User)
        .where(User.id == session_obj.user_id)
        .options(joinedload(User.profession))
    )
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user


session_auth_dep = Annotated[User, Depends(get_current_user_session)]


async def get_current_user_jwt(
    session: AsyncSession = Depends(db_dep),
    credentials: HTTPAuthorizationCredentials = Depends(jwt_security),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing bearer token.")

    token = credentials.credentials.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    if token.count(".") != 2:
        raise HTTPException(
            status_code=401,
            detail="Malformed JWT. Use only the raw access token value.",
        )

    decoded = decode_jwt_token(token)
    raw_user_id = decoded.get("sub")
    if raw_user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload.")

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token subject.")

    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    if exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired.")

    stmt = select(User).where(User.id == user_id).options(joinedload(User.profession))
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user


current_user_jwt_dep = Annotated[User, Depends(get_current_user_jwt)]
