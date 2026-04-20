import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.limiter import limiter
from app.tasks.scheduler import run_scheduler
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bookmarks import router as bookmarks_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.comments import router as comments_router
from app.api.v1.endpoints.follows import router as follows_router
from app.api.v1.endpoints.media import router as media_router
from app.api.v1.endpoints.moderation import router as moderation_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.posts import router as posts_router
from app.api.v1.endpoints.professions import router as professions_router
from app.api.v1.endpoints.revisions import router as revisions_router
from app.api.v1.endpoints.tags import router as tags_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.votes import router as votes_router
from app.api.v1.endpoints.search import router as search_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_scheduler())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="LibrHub", version="0.1.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(posts_router, prefix="/api/v1/posts", tags=["Posts"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(tags_router, prefix="/api/v1/tags", tags=["Tags"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["Comments"])
app.include_router(votes_router, prefix="/api/v1/votes", tags=["Votes"])
app.include_router(bookmarks_router, prefix="/api/v1/bookmarks", tags=["Bookmarks"])
app.include_router(follows_router, prefix="/api/v1/follows", tags=["Follows"])
app.include_router(professions_router, prefix="/api/v1/professions", tags=["Professions"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(revisions_router, prefix="/api/v1/revisions", tags=["Revisions"])
app.include_router(media_router, prefix="/api/v1/media", tags=["Media"])
app.include_router(moderation_router, prefix="/api/v1/moderation", tags=["Moderation"])
app.include_router(search_router, prefix="/api/v1/search", tags=["Search"])


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
