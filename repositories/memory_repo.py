from dataclasses import dataclass
from typing import Dict, Optional

from core.security import hash_password


@dataclass
class UserRecord:
    id: int
    name: str
    email: str
    password_hash: str


class MemoryRepo:
    def __init__(self) -> None:
        self.users_by_email: Dict[str, UserRecord] = {}
        self._seed()

    def _seed(self) -> None:
        # Seed ONE test user (password = Password@123)
        # hash generated using bcrypt; ** replace later from DB
        # repositories/memory_repo.py
        seeded = UserRecord(
            id=1,
            name="Test User",
            email="test@ampify.com",
            password_hash=hash_password("Password@123"),
        )
        self.users_by_email[seeded.email] = seeded

    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        return self.users_by_email.get(email.strip().lower())


repo = MemoryRepo()
