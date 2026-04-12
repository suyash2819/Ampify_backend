from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import API_PREFIX
from routers import auth

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in production: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Hello World"}
