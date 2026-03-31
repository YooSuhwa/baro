import redis.asyncio as aioredis

from app.config import settings

redis_pool = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> aioredis.Redis:
    return redis_pool
