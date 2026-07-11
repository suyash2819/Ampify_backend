import logging
from typing import List, Optional
from uuid import UUID
from connection.cockroachDB import get_connection
from schemas.song import SongOut

logger = logging.getLogger(__name__)


class SongsRepository:
    """Repository for song operations with CockroachDB."""

    def get_all_songs(self) -> List[SongOut]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, file_path, file_type, artist_id, genre_id
                    FROM songs
                    ORDER BY name
                """)

                results = cur.fetchall()

                if results:
                    songs = []
                    for row in results:
                        songs.append(
                            SongOut(
                                id=str(row[0]),
                                name=row[1],
                                file_path=row[2],
                                file_type=row[3],
                                artist_id=str(row[4]) if row[4] else None,
                                genre_id=str(row[5]) if row[5] else None,
                            )
                        )
                    return songs
                return []

        except Exception as e:
            logger.error(f"Error retrieving songs: {e}")
            raise
        finally:
            conn.close()

    def get_song_by_id(self, song_id: str) -> Optional[SongOut]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, file_path, file_type, artist_id, genre_id
                    FROM songs
                    WHERE id = %s
                """, (song_id,))
                
                result = cur.fetchone()
                print(f"Retrieved song by id {song_id}: {result}")  # Debugging line
                if result:
                    return SongOut(
                        id=str(result[0]),
                        name=result[1],
                        file_path=result[2],
                        file_type=result[3],
                        artist_id=str(result[4]) if result[4] else None,
                        genre_id=str(result[5]) if result[5] else None,
                    )
                return None

        except Exception as e:
            logger.error(f"Error retrieving song by id: {e}")
            raise
        finally:
            conn.close()

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
