from fastapi import FastAPI
from connection.rds import RdsConnection

app = FastAPI()
rdsConnection=RdsConnection() 

@app.get("/")
async def root():
    return {"message": "Hello World"}