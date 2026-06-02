import logging
from typing import List, Optional

from connection.cockroachDB import get_connection
from schemas.genre import GenreOut

logger = logging.getLogger(__name__)


class GenresRepository:
    """Repository for genre operations with CockroachDB."""

    def get_all_genres(self) -> List[GenreOut]:
        """Retrieve all genres with id and name."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name
                    FROM genres
                    ORDER BY name
                """)
                
                results = cur.fetchall()
                
                if results:
                    return [
                        GenreOut(id=row[0], name=row[1])
                        for row in results
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving genres: {e}")
            raise
        finally:
            conn.close()

    def get_genre_by_id(self, genre_id: int) -> Optional[GenreOut]:
        """Retrieve genre by id."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name
                    FROM genres
                    WHERE id = %s
                """, (genre_id,))
                
                result = cur.fetchone()
                
                if result:
                    return GenreOut(id=result[0], name=result[1])
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving genre: {e}")
            raise
        finally:
            conn.close()
