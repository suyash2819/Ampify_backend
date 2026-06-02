import logging
from typing import List

from connection.cockroachDB import get_connection
from schemas.preference import PreferencePayload, PreferenceResponse

logger = logging.getLogger(__name__)


class PreferencesRepository:
    """Repository for preference operations with CockroachDB."""

    def save_preferences(self, user_id: str, preferences: List[PreferencePayload]) -> List[PreferenceResponse]:
        """Save multiple preferences for a user."""
        conn = get_connection()
        saved_preferences = []
        
        try:
            with conn.cursor() as cur:
                for pref in preferences:
                    cur.execute("""
                        INSERT INTO preferences (user_id, genre_id, artist_id)
                        VALUES (%s, %s, %s)
                        RETURNING id, user_id, genre_id, artist_id
                    """, (pref.user_id, pref.genre_id, pref.artist_id))
                    
                    result = cur.fetchone()
                    
                    if result:
                        saved_preferences.append(
                            PreferenceResponse(
                                id=result[0],
                                user_id=result[1],
                                genre_id=result[2],
                                artist_id=result[3]
                                
                            )
                        )
                
                conn.commit()
                return saved_preferences
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error saving preferences: {e}")
            raise
        finally:
            conn.close()

    def get_user_preferences(self, user_id: str) -> List[PreferenceResponse]:
        """Retrieve all preferences for a specific user."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, user_id, genre_id, artist_id, created_at
                    FROM preferences
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
                
                results = cur.fetchall()
                
                if results:
                    return [
                        PreferenceResponse(
                            id=row[0],
                            user_id=row[1],
                            genre_id=row[2],
                            artist_id=row[3],
                            created_at=row[4]
                        )
                        for row in results
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving preferences: {e}")
            raise
        finally:
            conn.close()

    def delete_preference(self, preference_id: str, user_id: str) -> bool:
        """Delete a specific preference - only if owned by the user."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM preferences
                    WHERE id = %s AND user_id = %s
                """, (preference_id, user_id))
                
                conn.commit()
                return cur.rowcount > 0
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error deleting preference: {e}")
            raise
        finally:
            conn.close()
