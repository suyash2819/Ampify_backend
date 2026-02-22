from fastapi import FastAPI

# from connection.rds import RdsConnection
from routers import api_router

app = FastAPI()
# rdsConnection = RdsConnection()
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
