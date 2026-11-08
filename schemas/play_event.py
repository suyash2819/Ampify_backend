from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field


class PlayEventCreate(BaseModel):
    event_id: UUID
    event_type: Literal["play_ended"] = Field(alias="type")
    track_id: str = Field(min_length=1)
    started_at: AwareDatetime
    ms_played: int = Field(ge=0)
    track_duration_ms: int = Field(gt=0)
    end_reason: Literal["finished", "skipped", "closed", "error"]
    context_type: str | None = None
    context_id: str | None = None
    source: Literal["user", "agent"] = "user"
    session_id: str | None = None
    queue_instance_id: str | None = None
    device: str | None = None
    app_version: str | None = None


class PlayEventsSaveResponse(BaseModel):
    inserted: int
    duplicates: int
