import psycopg2
import psycopg2.extras

def create_tables():
    conn = None
    try:
        conn = connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")
        conn.commit()
    finally:
        if conn:
            conn.close()
def connection():
    return psycopg2.connect(
            dsn=f"postgres://default:8K5kOACdQJsu@ep-muddy-night-a1n4kkf1.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=false"
        )
