from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, Response
import mimetypes
import logging

from repositories.songs_repo import SongsRepository
from connection.gcp_storage import storage_client

logger = logging.getLogger(__name__)

router = APIRouter()
repo = SongsRepository()


@router.get("/songs")
def list_songs():
    return repo.get_all_songs()


@router.get("/songs/{song_id}/stream")
def stream_song(song_id: str, request: Request):
    song = repo.get_song_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    blob_name = song.file_path
    # Prefer stored file_type (MIME) from DB when available
    mime_type = song.file_type or mimetypes.guess_type(song.file_name)[0] or "application/octet-stream"

    # Get total size
    try:
        total_size = storage_client.get_blob_size(blob_name)
    except Exception as e:
        logger.error(f"Failed to get blob size for {blob_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to access storage")

    range_header = request.headers.get("range")

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Disposition": f'inline; filename="{song.file_name}"',
    }

    if range_header is None:
        # Full content
        try:
            generator = storage_client.stream_blob(blob_name)
        except Exception as e:
            logger.error(f"Failed to stream blob {blob_name}: {e}")
            raise HTTPException(status_code=500, detail="Failed to access storage")

        headers["Content-Length"] = str(total_size)
        return StreamingResponse(generator, media_type=mime_type, headers=headers)

    # Handle Range requests: expected format 'bytes=start-end' or 'bytes=start-'
    try:
        units, ranges = range_header.split("=", 1)
        if units.strip().lower() != "bytes":
            raise ValueError("Unsupported range unit")
        start_str, end_str = ranges.split("-", 1)
        start = int(start_str) if start_str != "" else None
        end = int(end_str) if end_str != "" else None
    except Exception:
        # Malformed Range header
        raise HTTPException(status_code=400, detail="Invalid Range header")

    if start is None:
        # suffix byte-range: '-N' meaning the last N bytes
        suffix_length = end
        if suffix_length is None:
            raise HTTPException(status_code=400, detail="Invalid Range header")
        if suffix_length <= 0:
            raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")
        start = max(total_size - suffix_length, 0)
        end = total_size - 1
    else:
        if end is None:
            end = total_size - 1

    # Validate range
    if start >= total_size or start < 0 or end < start:
        # 416
        content_range = f"bytes */{total_size}"
        return Response(status_code=416, headers={"Content-Range": content_range})

    # Clamp end
    end = min(end, total_size - 1)
    content_length = end - start + 1

    try:
        generator = storage_client.stream_blob_range(blob_name, start=start, end=end)
    except Exception as e:
        logger.error(f"Failed to stream blob range {blob_name} ({start}-{end}): {e}")
        raise HTTPException(status_code=500, detail="Failed to access storage")

    headers["Content-Range"] = f"bytes {start}-{end}/{total_size}"
    headers["Content-Length"] = str(content_length)

    return StreamingResponse(generator, status_code=206, media_type=mime_type, headers=headers)
