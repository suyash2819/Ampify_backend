from pydantic import BaseModel, Field
from typing import List


class ArtistOut(BaseModel):
    """Schema for artist response."""
    id: str
    name: str

    class Config:
        from_attributes = True


class ArtistListResponse(BaseModel):
    """Schema for list of artists response."""
    artists: List[ArtistOut]
