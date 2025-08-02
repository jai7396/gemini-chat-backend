import os
import psycopg2
from urllib.parse import urlparse

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise Exception("DATABASE_URL environment variable not set")

result = urlparse(db_url)

conn = psycopg2.connect(
    database=result.path[1:],      
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)
