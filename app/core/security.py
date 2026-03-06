import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from jwt import InvalidTokenError
from app.core.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_slug(title):
    return title.lower().replace(" ", "-")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def generate_jwt_tokens(user_id: int, is_access_only: bool = False):
    access_token = jwt.encode(
        payload={
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    if is_access_only:
        return access_token

    refresh_token = jwt.encode(
        payload={
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        },
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return access_token, refresh_token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


def send_email(to_email: str, subject: str, body: str):
    if not all(
        [
            settings.EMAIL_ADDRESS,
            settings.EMAIL_PASSWORD,
            settings.SMTP_SERVER,
            settings.SMTP_PORT,
        ]
    ):
        raise HTTPException(
            status_code=500,
            detail="Email settings are not configured in environment variables.",
        )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["Body"] = body
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)
