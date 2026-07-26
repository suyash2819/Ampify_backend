from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SongBase(BaseModel):
    name: str  
    artist_id: UUID
    genre_id: Optional[UUID] = None
    file_path: str  
    file_typ: Optional[str] = None  
    image_url: Optional[str] = None 

class SongCreate(SongBase):
    pass

class SongOut(BaseModel):
    id: UUID
    title: str 
    artist: str 
    image_url: Optional[str] = None
    song_url: str 
    file_type: Optional[str] = None
    genre_id: Optional[UUID] = None
    class Config:
        from_attributes = True
