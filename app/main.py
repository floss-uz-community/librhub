from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints.users import router as users_router

app = FastAPI(title="LibrHub", version="0.1.0")
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
