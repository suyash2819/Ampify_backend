from pydantic import BaseModel, EmailStr, Field


class SigninRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
