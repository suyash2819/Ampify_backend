import os
from dotenv import load_dotenv

load_dotenv()

API_VERSION=os.getenv("API_VERSION", "v1")
API_PREFIX = os.getenv("API_V1_PREFIX", "/api/"+API_VERSION)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "test")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# GCP Storage Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "ampify-1")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME", "ampify-assets")
