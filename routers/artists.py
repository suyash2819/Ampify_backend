from fastapi import APIRouter, HTTPException, status
import logging

from repositories.artists_repo import ArtistsRepository
from schemas.artist import ArtistListResponse, ArtistOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/artists", tags=["artists"])

artists_repo = ArtistsRepository()


@router.get("/", response_model=ArtistListResponse)
def get_artists():
    """Get list of all artists."""
    try:
        artists = artists_repo.get_all_artists()
        return ArtistListResponse(artists=artists)
    except Exception as e:
        logger.error(f"Error fetching artists: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch artists"
        )


@router.get("/{artist_id}", response_model=ArtistOut)
def get_artist(artist_id: int):
    """Get artist by id."""
    try:
        artist = artists_repo.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artist with id {artist_id} not found"
            )
        return artist
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching artist: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch artist"
        )