from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bookmarks import router as bookmarks_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.comments import router as comments_router
from app.api.v1.endpoints.follows import router as follows_router
from app.api.v1.endpoints.media import router as media_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.posts import router as posts_router
from app.api.v1.endpoints.professions import router as professions_router
from app.api.v1.endpoints.revisions import router as revisions_router
from app.api.v1.endpoints.tags import router as tags_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.votes import router as votes_router

app = FastAPI(title="LibrHub", version="0.1.0")
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


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
