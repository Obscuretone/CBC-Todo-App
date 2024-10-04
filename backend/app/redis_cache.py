import aioredis
import os


async def get_redis_connection():
    # Fetch the Redis URL from environment variables or use the default if not set
    redis_url = os.getenv("REDIS_URI", "redis://localhost:6379/0")

    # Create and return a Redis connection using aioredis
    redis = await aioredis.from_url(redis_url, decode_responses=True)

    return redis
