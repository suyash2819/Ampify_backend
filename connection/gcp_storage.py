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

# Singleton instance to be used across the app
storage_client = GCPStorageClient()
