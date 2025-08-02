import redis

redis = redis.Redis(
    host="localhost",  # or your Redis container name
    port=6379,
    db=0,
    decode_responses=True  # so values are str, not bytes
)
