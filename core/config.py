import os

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "test")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
