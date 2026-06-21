from google.cloud import storage
import logging
from core.config import GCP_PROJECT_ID, GCP_BUCKET_NAME

logger = logging.getLogger(__name__)

class GCPStorageClient:
    def __init__(self):
        try:
            self.client = storage.Client(project=GCP_PROJECT_ID)
            self.bucket_name = GCP_BUCKET_NAME
            self.bucket = self.client.bucket(self.bucket_name)
            logger.info(f"Initialized GCP Storage Client for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GCP Storage Client: {e}")
            self.client = None
            self.bucket = None

    def upload_file(self, file_path: str, destination_blob_name: str) -> str:
        """Uploads a file to the bucket."""
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")
            
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)
            logger.info(f"File {file_path} uploaded to {destination_blob_name}.")
            return blob.public_url
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise e

    def upload_from_string(self, data: bytes, destination_blob_name: str, content_type: str = None) -> str:
        """Uploads a file from memory to the bucket."""
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")
            
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_string(data, content_type=content_type)
            logger.info(f"Data uploaded to {destination_blob_name}.")
            return blob.public_url
        except Exception as e:
            logger.error(f"Error uploading data: {e}")
            raise e

    def download_file(self, source_blob_name: str, destination_file_name: str):
        """Downloads a blob from the bucket."""
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")
            
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            logger.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            raise e

    def delete_file(self, blob_name: str):
        """Deletes a blob from the bucket."""
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")
            
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            logger.info(f"Blob {blob_name} deleted.")
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise e

    def stream_blob(self, source_blob_name: str, chunk_size: int = 262144):
        """Stream a blob from the bucket in chunks.

        Yields bytes chunks suitable for use with StreamingResponse.
        """
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")

        try:
            blob = self.bucket.blob(source_blob_name)
            # Use the blob as a file-like object for streaming
            with blob.open("rb") as stream:
                while True:
                    chunk = stream.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            logger.error(f"Error streaming blob {source_blob_name}: {e}")
            raise e

    def get_blob_size(self, source_blob_name: str) -> int:
        """Return the size in bytes for the given blob."""
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")

        try:
            blob = self.bucket.get_blob(source_blob_name)
            if not blob:
                raise Exception(f"Blob {source_blob_name} not found")
            return blob.size
        except Exception as e:
            logger.error(f"Error getting blob size for {source_blob_name}: {e}")
            raise e

    def stream_blob_range(self, source_blob_name: str, start: int = 0, end: int = None, chunk_size: int = 262144):
        """Stream a byte range [start, end] from the blob.

        If `end` is None, streams until EOF. `end` is inclusive.
        """
        if not self.bucket:
            raise Exception("GCP Storage Client not initialized.")

        try:
            blob = self.bucket.blob(source_blob_name)
            with blob.open("rb") as stream:
                stream.seek(start)
                bytes_remaining = None
                if end is not None:
                    # end is inclusive, compute bytes to read
                    bytes_remaining = end - start + 1

                while True:
                    read_size = chunk_size if bytes_remaining is None else min(chunk_size, bytes_remaining)
                    if read_size <= 0:
                        break
                    chunk = stream.read(read_size)
                    if not chunk:
                        break
                    yield chunk
                    if bytes_remaining is not None:
                        bytes_remaining -= len(chunk)
                        if bytes_remaining <= 0:
                            break
        except Exception as e:
            logger.error(f"Error streaming blob range {source_blob_name} ({start}-{end}): {e}")
            raise e

# Singleton instance to be used across the app
storage_client = GCPStorageClient()
