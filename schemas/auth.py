from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class SigninRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SignupResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
