import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.enums import PostStatus
from app.models.post import Post

logger = logging.getLogger(__name__)


async def _publish_scheduled_posts() -> None:
    async with SessionLocal() as db:
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(Post).where(
                Post.status == PostStatus.SCHEDULED,
                Post.scheduled_at <= now,
            )
        )
        posts = result.scalars().all()

        if not posts:
            return

        for post in posts:
            post.status = PostStatus.PUBLISHED
            post.published_at = now

        await db.commit()
        logger.info("Published %d scheduled post(s).", len(posts))


async def run_scheduler() -> None:
    while True:
        try:
            await _publish_scheduled_posts()
        except Exception:
            logger.exception("Scheduler error while publishing scheduled posts.")
        await asyncio.sleep(60)
