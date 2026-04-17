import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL)


def check_rate_limit(user_id: str) -> None:
    """
    Implement sliding window rate limiting.
    Limit: RATE_LIMIT_PER_MINUTE requests per user per minute.
    Raises HTTPException(429) if exceeded.
    """
    key = f"rate:{user_id}"
    current = int(r.get(key) or 0)

    if current >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} requests per minute."
        )

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60)
    pipe.execute()
