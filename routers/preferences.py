from fastapi import APIRouter, HTTPException, status, Depends
import logging

from repositories.preferences_repo import PreferencesRepository
from schemas.preference import PreferenceRequest, PreferencesSaveResponse, PreferenceResponse
from core.deps import get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/preferences", tags=["preferences"])

preferences_repo = PreferencesRepository()


@router.post("/", response_model=PreferencesSaveResponse)
def save_preferences(payload: PreferenceRequest, current_user_id: str = Depends(get_current_user_id)):
    """Save user preferences from UI. Requires authentication."""
    try:
        if not payload.preferences:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Preferences list cannot be empty"
            )
        
        saved_prefs = preferences_repo.save_preferences(current_user_id, payload.preferences)
        
        return PreferencesSaveResponse(
            message="Preferences saved successfully",
            count=len(saved_prefs),
            preferences=saved_prefs
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save preferences"
        )


@router.get("/", response_model=list[PreferenceResponse])
def get_user_preferences(current_user_id: str = Depends(get_current_user_id)):
    """Get all preferences for the authenticated user."""
    try:
        preferences = preferences_repo.get_user_preferences(current_user_id)
        return preferences
    except Exception as e:
        logger.error(f"Error fetching preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch preferences"
        )


@router.delete("/{preference_id}", status_code=status.HTTP_200_OK)
def delete_preference(preference_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Delete a specific preference. Only the owner can delete."""
    try:
        deleted = preferences_repo.delete_preference(preference_id, current_user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Preference with id {preference_id} not found or you don't have permission to delete it"
            )
        
        return {"message": "Preference deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting preference: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete preference"
        )
