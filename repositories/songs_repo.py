import logging
from typing import List, Optional

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
