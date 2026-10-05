import json
from typing import Any

from fastapi import APIRouter, Body, Depends

from connection.redis import get_redis_connection
from core.deps import get_current_user_id
from repositories.songs_repo import songs_repo

router = APIRouter(prefix="/queue", tags=["queue"])


@router.get("")
def get_queue(user_id: str = Depends(get_current_user_id)):
	redis = get_redis_connection()
	queue = redis.get(f"queue:{user_id}")
	if queue is None:
		return []

	queue_data = json.loads(queue)
	if isinstance(queue_data, dict):
		song_ids = queue_data.get("songIds", [])
		queue_data["songs"] = songs_repo.get_songs_by_ids(song_ids if isinstance(song_ids, list) else [])
	return queue_data


@router.post("")
def save_queue(
	queue: Any = Body(...),
	user_id: str = Depends(get_current_user_id),
):
	redis = get_redis_connection()
	redis.set(f"queue:{user_id}", json.dumps(queue))
	return {"message": "Queue saved successfully"}
