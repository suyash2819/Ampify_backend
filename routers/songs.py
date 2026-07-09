from fastapi import APIRouter, Depends, Query
from typing import List
from repositories.songs_repo import songs_repo
from schemas.song import SongOut
from core.deps import get_current_user_id

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get("/search", response_model=List[SongOut])
def search_songs(query: str = Query(..., min_length=1)):
    """Search for songs by title or artist name."""
    return songs_repo.search_songs(query)

@router.get("/suggestions", response_model=List[SongOut])
def get_suggestions(user_id: str = Depends(get_current_user_id)):
    """Get song suggestions based on user preferences."""
    return songs_repo.get_suggested_songs(user_id)
