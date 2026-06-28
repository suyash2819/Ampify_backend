import logging
from typing import List, Optional
from uuid import UUID
from connection.cockroachDB import get_connection
from schemas.song import SongOut

logger = logging.getLogger(__name__)

class SongsRepository:
    def search_songs(self, query: str) -> List[SongOut]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Search by song name OR artist name
                cur.execute("""
                    SELECT s.id, s.name, a.name as artist_name, s.image_url, s.file_path, s.file_type
                    FROM songs s
                    LEFT JOIN artists a ON s.artist_id = a.id
                    WHERE s.name ILIKE %s OR a.name ILIKE %s
                    LIMIT 20
                """, (f"%{query}%", f"%{query}%"))
                
                rows = cur.fetchall()
                return [
                    SongOut(
                        id=row[0], 
                        title=row[1], 
                        artist=row[2] or "Unknown Artist", 
                        image_url=row[3], 
                        song_url=row[4],
                        file_type=row[5]
                    ) for row in rows
                ]
        except Exception as e:
            logger.error(f"Error searching songs: {e}")
            return []
        finally:
            conn.close()

    def get_suggested_songs(self, user_id: str, limit: int = 5) -> List[SongOut]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Get songs matching user's preferred genres or artists
                cur.execute("""
                    SELECT s.id, s.name, a.name as artist_name, s.image_url, s.file_path, s.file_type
                    FROM songs s
                    LEFT JOIN artists a ON s.artist_id = a.id
                    WHERE s.genre_id IN (SELECT genre_id FROM preferences WHERE user_id = %s)
                       OR s.artist_id IN (SELECT artist_id FROM preferences WHERE user_id = %s)
                    ORDER BY RANDOM()
                    LIMIT %s
                """, (user_id, user_id, limit))
                
                rows = cur.fetchall()
                
                # If no preferences yet, return random songs
                if not rows:
                    cur.execute("""
                        SELECT s.id, s.name, a.name as artist_name, s.image_url, s.file_path, s.file_type
                        FROM songs s
                        LEFT JOIN artists a ON s.artist_id = a.id
                        ORDER BY RANDOM()
                        LIMIT %s
                    """, (limit,))
                    rows = cur.fetchall()

                return [
                    SongOut(
                        id=row[0], 
                        title=row[1], 
                        artist=row[2] or "Unknown Artist", 
                        image_url=row[3], 
                        song_url=row[4],
                        file_type=row[5]
                    ) for row in rows
                ]
        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return []
        finally:
            conn.close()

songs_repo = SongsRepository()
