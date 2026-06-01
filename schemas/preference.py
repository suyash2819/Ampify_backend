from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PreferencePayload(BaseModel):
    """Schema for a single preference item."""
    user_id: str
    genre_id: Optional[str] = None
    artist_id: Optional[str] = None


class PreferenceRequest(BaseModel):
    """Schema for preferences POST request - array of preferences."""
    preferences: List[PreferencePayload]


class PreferenceResponse(BaseModel):
    """Schema for preference response."""
    id: str
    user_id: str
    genre_id: Optional[str] = None
    artist_id: Optional[str] = None

    class Config:
        from_attributes = True


class PreferencesSaveResponse(BaseModel):
    """Schema for preferences save response."""
    message: str
    count: int
    preferences: List[PreferenceResponse]
