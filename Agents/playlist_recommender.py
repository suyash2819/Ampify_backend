import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from repositories.recommendations_repo import recommendations_repo

logger = logging.getLogger(__name__)

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SYSTEM_PROMPT = (
    "You are a music recommendation curator. Use the user's recent play events "
    "and each song's mood to select three candidate tracks. A finished "
    "play is a positive signal, a skipped play is a negative signal, and closed "
    "or error events are neutral. Never select a track marked previously_skipped "
    "or listed in skipped_tracks. Treat skipped moods as negative preferences "
    "and avoid recommending those moods when other candidates are available. "
    "Prefer moods from finished plays, and avoid repeating recent plays when "
    "other candidates are available. Return only track IDs from the provided "
    "candidates and a brief reason."
)


class QueuePick(BaseModel):
    track_ids: list[str] = Field(description="Track IDs from the candidate songs")
    reason: str = Field(description="One short sentence explaining the choice")


def pick_next(user_id: str, limit: int = 3) -> QueuePick:
    """Recommend songs using the user's play history and catalog moods."""
    context = recommendations_repo.get_recommendation_context(
        user_id, candidate_limit=max(limit * 10, 30)
    )
    candidates = context["candidates"]
    if not candidates:
        return QueuePick(track_ids=[], reason="No songs with mood data are available.")

    api_key = os.getenv("GROQ_KEY")
    if not api_key:
        raise RuntimeError("GROQ_KEY is required to generate playlist recommendations")

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        api_key=api_key,
        temperature=0.3,
        max_retries=2,
    )
    structured_model = model.with_structured_output(QueuePick)
    pick = structured_model.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", json.dumps(context, ensure_ascii=True)),
        ]
    )
    if not isinstance(pick, QueuePick):
        pick = QueuePick.model_validate(pick)

    candidate_ids = {candidate["track_id"] for candidate in candidates}
    skipped_ids = {track["track_id"] for track in context["skipped_tracks"]}
    valid_ids = list(
        dict.fromkeys(
            track_id
            for track_id in pick.track_ids
            if track_id in candidate_ids and track_id not in skipped_ids
        )
    )[:limit]
    if not valid_ids:
        logger.error("Recommendation model returned no valid candidate track IDs")
        raise ValueError("Recommendation model returned no valid candidate track IDs")
    if len(valid_ids) != len(pick.track_ids):
        logger.warning("Removed invalid or duplicate IDs from recommendation output")

    print(
        f"Generated recommendations: track_ids={valid_ids}; reason={pick.reason}",
        flush=True,
    )
    return QueuePick(track_ids=valid_ids, reason=pick.reason)
