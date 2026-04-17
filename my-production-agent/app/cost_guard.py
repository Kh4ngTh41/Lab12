from datetime import datetime
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL)

ESTIMATED_COST_PER_REQUEST = 0.01


def check_budget(user_id: str) -> None:
    """
    Check monthly budget cho user.
    Limit: MONTHLY_BUDGET_USD per user per month.
    Raises HTTPException(402) if exceeded.
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"

    current = float(r.get(key) or 0)

    if current + ESTIMATED_COST_PER_REQUEST > settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=402,
            detail=f"Budget exceeded. Monthly limit: ${settings.MONTHLY_BUDGET_USD}"
        )

    r.incrbyfloat(key, ESTIMATED_COST_PER_REQUEST)
    r.expire(key, 32 * 24 * 3600)
