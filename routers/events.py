import logging

from fastapi import APIRouter, Depends, HTTPException, status

from core.deps import get_current_user_id
from repositories.play_events_repo import PlayEventsRepository
from schemas.play_event import PlayEventCreate, PlayEventsSaveResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/events", tags=["events"])
play_events_repo = PlayEventsRepository()


@router.post("", response_model=PlayEventsSaveResponse)
def save_play_events(
    events: list[PlayEventCreate],
    user_id: str = Depends(get_current_user_id),
) -> PlayEventsSaveResponse:
    """Store play events for the authenticated user; repeated IDs are ignored."""
    try:
        inserted, duplicates = play_events_repo.save_events(user_id, events)
        return PlayEventsSaveResponse(inserted=inserted, duplicates=duplicates)
    except Exception as exc:
        logger.exception("Failed to save play events")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save play events",
        ) from exc
