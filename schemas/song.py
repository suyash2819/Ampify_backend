from pydantic import BaseModel
<<<<<<< HEAD
from typing import Optional


class SongOut(BaseModel):
    id: str
    name: str
    file_path: str
    file_type: Optional[str] = None
    artist_id: Optional[str] = None
    genre_id: Optional[str] = None
=======
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

    class Config:
        from_attributes = True
>>>>>>> 99c834fd7d45777a0645203e0da815f1969ed279
