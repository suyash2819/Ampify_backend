import logging
from typing import List, Optional

from connection.cockroachDB import get_connection
from schemas.artist import ArtistOut

logger = logging.getLogger(__name__)


class ArtistsRepository:
    """Repository for artist operations with CockroachDB."""

    def get_all_artists(self) -> List[ArtistOut]:
        """Retrieve all artists with id and name."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name
                    FROM artists
                    ORDER BY name
                """)
                
                results = cur.fetchall()
                
                if results:
                    return [
                        ArtistOut(id=row[0], name=row[1])
                        for row in results
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving artists: {e}")
            raise
        finally:
            conn.close()

    def get_artist_by_id(self, artist_id: int) -> Optional[ArtistOut]:
        """Retrieve artist by id."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name
                    FROM artists
                    WHERE id = %s
                """, (artist_id,))
                
                result = cur.fetchone()
                
                if result:
                    return ArtistOut(id=result[0], name=result[1])
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving artist: {e}")
            raise
        finally:
            conn.close()
