import redis
from rq import Queue
from app.config import REDIS_URL


redis_conn = redis.from_url(REDIS_URL)
queue = Queue("gemini", connection=redis_conn)
