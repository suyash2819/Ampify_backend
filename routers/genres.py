from fastapi import APIRouter, HTTPException, status
import logging

from repositories.genres_repo import GenresRepository
from schemas.genre import GenreListResponse, GenreOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/genres", tags=["genres"])

genres_repo = GenresRepository()


@router.get("/", response_model=GenreListResponse)
def get_genres():
    """Get list of all genres."""
    try:
        genres = genres_repo.get_all_genres()
        return GenreListResponse(genres=genres)
    except Exception as e:
        logger.error(f"Error fetching genres: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch genres"
        )


@router.get("/{genre_id}", response_model=GenreOut)
def get_genre(genre_id: int):
    """Get genre by id."""
    try:
        genre = genres_repo.get_genre_by_id(genre_id)
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with id {genre_id} not found"
            )
        return genre
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch genre"
        )