from pydantic import BaseModel, Field
from typing import List


class GenreOut(BaseModel):
    """Schema for genre response."""
    id: str
    name: str

    class Config:
        from_attributes = True


class GenreListResponse(BaseModel):
    """Schema for list of genres response."""
    genres: List[GenreOut]
