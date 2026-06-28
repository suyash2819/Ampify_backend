import logging
from typing import List, Optional
from uuid import UUID
from connection.cockroachDB import get_connection
from schemas.playlist import PlaylistOut, PlaylistCreate
from schemas.song import SongOut

logger = logging.getLogger(__name__)

class PlaylistsRepository:
    def get_user_playlists(self, user_id: str) -> List[PlaylistOut]:
        conn = get_connection()
        playlists = []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, user_id, name, description, image_url, created_at, updated_at
                    FROM playlists
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
                
                playlist_rows = cur.fetchall()
                
                for p_row in playlist_rows:
                    p_id = p_row[0]
                    # Fetch songs for this playlist
                    cur.execute("""
                        SELECT s.id, s.name, a.name as artist_name, s.image_url, s.file_path, s.file_type
                        FROM songs s
                        JOIN playlist_songs ps ON s.id = ps.song_id
                        LEFT JOIN artists a ON s.artist_id = a.id
                        WHERE ps.playlist_id = %s
                    """, (p_id,))
                    
                    song_rows = cur.fetchall()
                    songs = [
                        SongOut(
                            id=row[0], 
                            title=row[1], 
                            artist=row[2] or "Unknown Artist", 
                            image_url=row[3], 
                            song_url=row[4],
                            file_type=row[5]
                        ) for row in song_rows
                    ]
                    
                    playlists.append(PlaylistOut(
                        id=p_row[0], user_id=p_row[1], name=p_row[2],
                        description=p_row[3], image_url=p_row[4],
                        created_at=p_row[5], updated_at=p_row[6],
                        songs=songs
                    ))
            return playlists
        except Exception as e:
            logger.error(f"Error getting user playlists: {e}")
            raise
        finally:
            conn.close()

    def create_playlist(self, user_id: str, playlist: PlaylistCreate) -> PlaylistOut:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO playlists (user_id, name, description, image_url)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, user_id, name, description, image_url, created_at, updated_at
                """, (user_id, playlist.name, playlist.description, playlist.image_url))
                
                row = cur.fetchone()
                conn.commit()
                
                return PlaylistOut(
                    id=row[0], user_id=row[1], name=row[2],
                    description=row[3], image_url=row[4],
                    created_at=row[5], updated_at=row[6],
                    songs=[]
                )
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating playlist: {e}")
            raise
        finally:
            conn.close()

    def add_song_to_playlist(self, playlist_id: str, song_id: str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO playlist_songs (playlist_id, song_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (playlist_id, song_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Error adding song to playlist: {e}")
            return False
        finally:
            conn.close()

    def remove_song_from_playlist(self, playlist_id: str, song_id: str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM playlist_songs
                    WHERE playlist_id = %s AND song_id = %s
                """, (playlist_id, song_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Error removing song from playlist: {e}")
            return False
        finally:
            conn.close()

    def rename_playlist(self, playlist_id: str, user_id: str, new_name: str, new_description: Optional[str] = None) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE playlists 
                    SET name = %s, description = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND user_id = %s
                """, (new_name, new_description, playlist_id, user_id))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            logger.error(f"Error renaming playlist: {e}")
            return False
        finally:
            conn.close()

    def delete_playlist(self, playlist_id: str, user_id: str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM playlists
                    WHERE id = %s AND user_id = %s
                """, (playlist_id, user_id))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            logger.error(f"Error deleting playlist: {e}")
            return False
        finally:
            conn.close()

playlists_repo = PlaylistsRepository()
