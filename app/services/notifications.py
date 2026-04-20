import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import NotificationType
from app.models.notifications import Notification


async def create_notification(
    db: AsyncSession,
    *,
    recipient_user_id: int,
    actor_user_id: int | None,
    type: NotificationType,
    payload: dict,
) -> None:
    # Never notify the actor about their own actions
    if actor_user_id is not None and actor_user_id == recipient_user_id:
        return

    notification = Notification(
        recipient_user_id=recipient_user_id,
        actor_user_id=actor_user_id,
        type=type,
        payload=json.dumps(payload),
    )
    db.add(notification)
