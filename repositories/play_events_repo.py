from uuid import UUID

from connection.cockroachDB import get_connection
from schemas.play_event import PlayEventCreate


class PlayEventsRepository:
    """Repository for idempotent play-event ingestion."""

    def save_events(
        self, user_id: str, events: list[PlayEventCreate]
    ) -> tuple[int, int]:
        if not events:
            return 0, 0

        conn = get_connection()
        inserted = 0
        try:
            with conn.cursor() as cur:
                for event in events:
                    cur.execute(
                        """
                        INSERT INTO play_events (
                            event_id, user_id, track_id, started_at,
                            ms_played, track_duration_ms, end_reason,
                            context_type, context_id, source, session_id,
                            queue_instance_id, device, app_version
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (user_id, event_id) DO NOTHING
                        """,
                        (
                            str(event.event_id),
                            str(UUID(user_id)),
                            event.track_id,
                            event.started_at,
                            event.ms_played,
                            event.track_duration_ms,
                            event.end_reason,
                            event.context_type,
                            event.context_id,
                            event.source,
                            event.session_id,
                            event.queue_instance_id,
                            event.device,
                            event.app_version,
                        ),
                    )
                    if cur.rowcount:
                        inserted += 1

            conn.commit()
            return inserted, len(events) - inserted
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
