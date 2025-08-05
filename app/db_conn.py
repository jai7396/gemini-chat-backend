import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="Pandu@123",
    database="gemini_backend"
)
