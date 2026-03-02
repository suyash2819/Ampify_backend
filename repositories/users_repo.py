import uuid
import logging
from typing import Optional, List

from connection.cockroachDB import get_connection
from core.security import hash_password
from schemas.user import UserOut, UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UsersRepository:
    """Repository for user CRUD operations with CockroachDB."""

    def create_user(self, user_create: UserCreate) -> UserOut:
        """Create a new user with hashed password."""
        conn = get_connection()
        try:
            user_id = str(uuid.uuid4())
            password_hash = hash_password(user_create.password)
            
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (id, name, email, password_hash)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, name, email, password_hash, created_at, updated_at
                """, (user_id, user_create.name, user_create.email.strip().lower(), password_hash))
                
                result = cur.fetchone()
                conn.commit()
                
                if result:
                    return UserOut(
                        id=result[0],
                        name=result[1],
                        email=result[2],
                        created_at=result[4],
                        updated_at=result[5]
                    )
                    
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating user: {e}")
            raise
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[UserOut]:
        """Retrieve user by email."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, email, password_hash, created_at, updated_at
                    FROM users
                    WHERE email = %s
                """, (email.strip().lower(),))
                
                result = cur.fetchone()
                
                if result:
                    return UserOut(
                        id=result[0],
                        name=result[1],
                        email=result[2],
                        created_at=result[4],
                        updated_at=result[5]
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            raise
        finally:
            conn.close()

    def get_user_by_id(self, user_id: str) -> Optional[UserOut]:
        """Retrieve user by ID."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, email, password_hash, created_at, updated_at
                    FROM users
                    WHERE id = %s
                """, (user_id,))
                
                result = cur.fetchone()
                
                if result:
                    return UserOut(
                        id=result[0],
                        name=result[1],
                        email=result[2],
                        created_at=result[4],
                        updated_at=result[5]
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving user by ID: {e}")
            raise
        finally:
            conn.close()

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserOut]:
        """Update user information (name and/or email)."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Build update query dynamically
                updates = []
                params = []
                
                if user_update.name is not None:
                    updates.append("name = %s")
                    params.append(user_update.name)
                
                if user_update.email is not None:
                    updates.append("email = %s")
                    params.append(user_update.email.strip().lower())
                
                if not updates:
                    return self.get_user_by_id(user_id)
                
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(user_id)
                
                query = f"""
                    UPDATE users
                    SET {', '.join(updates)}
                    WHERE id = %s
                    RETURNING id, name, email, password_hash, created_at, updated_at
                """
                
                cur.execute(query, params)
                result = cur.fetchone()
                conn.commit()
                
                if result:
                    return UserOut(
                        id=result[0],
                        name=result[1],
                        email=result[2],
                        created_at=result[4],
                        updated_at=result[5]
                    )
                return None
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error updating user: {e}")
            raise
        finally:
            conn.close()

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by ID."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                return cur.rowcount > 0
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error deleting user: {e}")
            raise
        finally:
            conn.close()

    def list_all_users(self) -> List[UserOut]:
        """Retrieve all users."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, email, password_hash, created_at, updated_at
                    FROM users
                    ORDER BY created_at DESC
                """)
                
                results = cur.fetchall()
                users = []
                
                for result in results:
                    users.append(UserOut(
                        id=result[0],
                        name=result[1],
                        email=result[2],
                        created_at=result[4],
                        updated_at=result[5]
                    ))
                
                return users
                
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            raise
        finally:
            conn.close()


# Singleton instance for easy import
users_repo = UsersRepository()
