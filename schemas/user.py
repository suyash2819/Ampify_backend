from typing import List, NamedTuple, Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    """Schema for user response."""
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class UserRecord(NamedTuple):
    """Internal user record with password hash for authentication."""
    id: str
    name: str
    email: str
    password_hash: str
    created_at: str
    updated_at: str


class PreferencesRequest(BaseModel):
    artist_ids: List[int] = Field(default_factory=list)

class PreferencesOut(BaseModel):
    artist_ids: List[int]
