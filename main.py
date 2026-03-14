from fastapi import FastAPI

from core.config import API_PREFIX
from routers import auth

app = FastAPI()
app.include_router(auth.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Hello World"}
