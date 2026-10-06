from upstash_redis import Redis
import os


def get_redis_connection():
    """Establish and return a Redis connection."""
    return Redis(url=os.getenv("UPSTASH_REDIS_REST_URL"), token=os.getenv("UPSTASH_REDIS_REST_TOKEN"))

