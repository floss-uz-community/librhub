from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.comments import router as comments_router
from app.api.v1.endpoints.posts import router as posts_router
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


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
