from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="LibrHub", version="0.1.0")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")