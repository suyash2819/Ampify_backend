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
            
            # Create artists table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS artists (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    genre_id UUID,
                    country VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create genre table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS genre (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(100) NOT NULL UNIQUE
                )
            """)

            # Create songs table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
                    genre_id UUID REFERENCES genre(id) ON DELETE SET NULL,
                    file_path VARCHAR(512) NOT NULL,
                    file_type VARCHAR(50),
                    image_url VARCHAR(512),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create playlists table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    image_url VARCHAR(512),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create playlist_songs table (junction table)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS playlist_songs (
                    playlist_id UUID REFERENCES playlists(id) ON DELETE CASCADE,
                    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (playlist_id, song_id)
                )
            """)

            # Create preferences table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    genre_id UUID REFERENCES genre(id) ON DELETE CASCADE,
                    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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