from collections import Counter

from connection.cockroachDB import get_connection


class RecommendationsRepository:
    """Fetch user listening history and mood-matched song candidates."""

    def get_recommendation_context(
        self, user_id: str, candidate_limit: int = 30, history_limit: int = 50
    ) -> dict:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT pe.event_id::STRING, pe.track_id, s.name, s.mood,
                           pe.ms_played, pe.track_duration_ms,
                           pe.end_reason, pe.started_at
                    FROM play_events pe
                    LEFT JOIN songs s ON CAST(s.id AS STRING) = pe.track_id
                    WHERE pe.user_id = %s
                    ORDER BY pe.started_at DESC
                    LIMIT %s
                    """,
                    (user_id, history_limit),
                )
                history_rows = cur.fetchall()

                history = [
                    {
                        "event_id": row[0],
                        "track_id": row[1],
                        "title": row[2],
                        "mood": row[3],
                        "ms_played": row[4],
                        "track_duration_ms": row[5],
                        "end_reason": row[6],
                        "started_at": row[7].isoformat(),
                    }
                    for row in history_rows
                ]
                skipped_rows = [row for row in history_rows if row[6] == "skipped"]
                skipped_track_ids = {row[1] for row in skipped_rows}
                skipped_moods = Counter(
                    row[3].lower() for row in skipped_rows if row[3]
                )
                skipped_tracks = [
                    {
                        "track_id": row[1],
                        "title": row[2],
                        "mood": row[3],
                    }
                    for row in skipped_rows
                ]

                finished_plays = [
                    row for row in history_rows if row[6] == "finished" and row[3]
                ]
                mood_counts = Counter(row[3].lower() for row in finished_plays)
                target_mood = mood_counts.most_common(1)[0][0] if mood_counts else None

                cur.execute(
                    """
                    SELECT s.id::STRING, s.name, a.name, s.mood,
                           s.image_url, s.file_path, s.file_type
                    FROM songs s
                    LEFT JOIN artists a ON a.id = s.artist_id
                    WHERE s.mood IS NOT NULL
                    ORDER BY
                        CASE WHEN LOWER(s.mood) = LOWER(COALESCE(%s, '')) THEN 0 ELSE 1 END,
                        s.id
                    LIMIT %s
                    """,
                    (target_mood, candidate_limit),
                )
                candidates = [
                    {
                        "track_id": row[0],
                        "title": row[1],
                        "artist": row[2] or "Unknown Artist",
                        "mood": row[3],
                        "image_url": row[4],
                        "song_url": row[5],
                        "file_type": row[6],
                        "previously_skipped": row[0] in skipped_track_ids,
                    }
                    for row in cur.fetchall()
                ]

            return {
                "history": history,
                "skipped_tracks": skipped_tracks,
                "skipped_moods": dict(skipped_moods),
                "candidates": candidates,
                "target_mood": target_mood,
            }
        finally:
            conn.close()


recommendations_repo = RecommendationsRepository()
