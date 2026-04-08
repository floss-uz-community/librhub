from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep, pagination_dep
from app.db.session import get_db
from app.models.notifications import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter()


@router.get("/", response_model=list[NotificationResponse])
async def notifications_list(
    pagination: pagination_dep,
    unread_only: bool = Query(False),
    current_user: current_user_jwt_dep = ...,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Notification)
        .where(Notification.recipient_user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    )

    if unread_only:
        stmt = stmt.where(Notification.is_read == False)

    stmt = stmt.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{notification_id}/", response_model=NotificationResponse)
async def notification_detail(
    notification_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.recipient_user_id == current_user.id,
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        return JSONResponse(
            {"error": "Notification not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return notification


@router.patch("/{notification_id}/read/", response_model=NotificationResponse)
async def notification_mark_read(
    notification_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.recipient_user_id == current_user.id,
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    notification.is_read = True
    notification.read_at = datetime.now(timezone.utc)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


@router.patch("/read-all/")
async def notifications_mark_all_read(
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    await db.execute(
        update(Notification)
        .where(
            Notification.recipient_user_id == current_user.id,
            Notification.is_read == False,
        )
        .values(is_read=True, read_at=now)
    )
    await db.commit()
    return {"detail": "All notifications marked as read."}
