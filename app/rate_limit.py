from fastapi import HTTPException
from datetime import datetime, timedelta
from app.redis_conn import redis
from app.db_conn import conn

MAX_DAILY_MESSAGES = 5  # for Basic users

def get_user_subscription_tier(user_id: str) -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT subscription_tier FROM Users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        return result[0] if result else "Basic"  # fallback default

def check_rate_limit(user_id: str):
    today = datetime.utcnow().date()
    key = f"msgcount:{user_id}:{today}"
    
    count = redis.get(key)
    count = int(count) if count else 0

    if count >= MAX_DAILY_MESSAGES:
        raise HTTPException(
            status_code=429,
            detail="Daily message limit reached (Basic tier). Upgrade to Pro for unlimited access."
        )

    # Increment or set counter with expiry until midnight 
    if not count:
        tomorrow = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        ttl = int((tomorrow - datetime.utcnow()).total_seconds())
        redis.setex(key, ttl, 1)
    else:
        redis.incr(key)
