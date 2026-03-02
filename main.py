from fastapi import FastAPI

from core.config import API_V1_PREFIX
from routers import auth

app = FastAPI()
# rdsConnection = RdsConnection()
app.include_router(auth.router, prefix=API_V1_PREFIX)
# init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}
