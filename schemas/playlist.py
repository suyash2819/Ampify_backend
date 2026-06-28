from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from schemas.song import SongOut

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistOut(PlaylistBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    songs: List[SongOut] = []

    class Config:
        from_attributes = True
