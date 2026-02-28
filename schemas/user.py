from typing import List

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: int
    name: str
    email: str


class PreferencesRequest(BaseModel):
    artist_ids: List[int] = Field(default_factory=list)


class PreferencesOut(BaseModel):
    artist_ids: List[int]
