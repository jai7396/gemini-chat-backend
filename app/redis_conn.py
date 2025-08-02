import os
import redis

redis_url = os.getenv("REDIS_URL")

if not redis_url:
    raise Exception("REDIS_URL environment variable not set")

redis_conn = redis.from_url(redis_url, decode_responses=True)
