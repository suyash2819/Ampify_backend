from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from repositories.playlists_repo import playlists_repo
from schemas.playlist import PlaylistOut, PlaylistCreate
from core.deps import get_current_user_id

router = APIRouter(prefix="/playlists", tags=["playlists"])

@router.get("", response_model=List[PlaylistOut])
def get_my_playlists(user_id: str = Depends(get_current_user_id)):
    """Fetch all playlists for the authenticated user."""
    return playlists_repo.get_user_playlists(user_id)

@router.post("", response_model=PlaylistOut)
def create_new_playlist(
    playlist: PlaylistCreate, 
    user_id: str = Depends(get_current_user_id)
):
    """Create a new playlist for the authenticated user."""
    return playlists_repo.create_playlist(user_id, playlist)

# ── Liked Songs endpoints ─────────────────────────────────────────────────────

@router.post("/liked-songs", response_model=PlaylistOut)
def get_or_create_liked_songs(user_id: str = Depends(get_current_user_id)):
    """Get (or auto-create) the current user's Liked Songs playlist."""
    return playlists_repo.get_or_create_liked_songs_playlist(user_id)

@router.get("/liked-songs/song-ids", response_model=List[str])
def get_liked_song_ids(user_id: str = Depends(get_current_user_id)):
    """Return the list of song IDs the user has liked."""
    return playlists_repo.get_liked_song_ids(user_id)

# ── Song add / remove ─────────────────────────────────────────────────────────

@router.post("/{playlist_id}/songs/{song_id}")
def add_song(
    playlist_id: str, 
    song_id: str, 
    user_id: str = Depends(get_current_user_id)
):
    """Add a song to a playlist."""
    success = playlists_repo.add_song_to_playlist(playlist_id, song_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not add song to playlist")
    return {"message": "Song added successfully"}

@router.delete("/{playlist_id}/songs/{song_id}")
def remove_song(
    playlist_id: str, 
    song_id: str, 
    user_id: str = Depends(get_current_user_id)
):
    """Remove a song from a playlist."""
    success = playlists_repo.remove_song_from_playlist(playlist_id, song_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not remove song from playlist")
    return {"message": "Song removed successfully"}

@router.put("/{playlist_id}")
def rename_playlist(
    playlist_id: str,
    playlist: PlaylistCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Rename/update a playlist (Liked Songs playlist cannot be renamed)."""
    success = playlists_repo.rename_playlist(playlist_id, user_id, playlist.name, playlist.description)
    if not success:
        raise HTTPException(status_code=400, detail="Could not update playlist")
    return {"message": "Playlist updated successfully"}

@router.delete("/{playlist_id}")
def delete_playlist(
    playlist_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a playlist (Liked Songs playlist cannot be deleted)."""
    success = playlists_repo.delete_playlist(playlist_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not delete playlist")
    return {"message": "Playlist deleted successfully"}
