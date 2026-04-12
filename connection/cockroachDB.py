import os
import psycopg2
import logging

logger = logging.getLogger(__name__)

os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:26257/defaultdb?sslmode=disable")
def get_connection():
    """Establish and return a CockroachDB connection."""
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    """Initialize the database by creating required tables."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info("Database tables initialized successfully")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()


# Get the connection
conn = get_connection()