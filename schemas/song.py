from pydantic import BaseModel
from typing import Optional


class SongOut(BaseModel):
    id: str
    name: str
    file_path: str
    file_type: Optional[str] = None
    artist_id: Optional[str] = None
    genre_id: Optional[str] = None
