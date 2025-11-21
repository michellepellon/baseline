"""
User management.
Simple in-memory user storage. In production, use a proper database.
"""

from dataclasses import dataclass
from typing import Optional

from backend.auth.security import get_password_hash, verify_password


@dataclass
class User:
    """User model."""

    username: str
    hashed_password: str


# In-memory user storage
# TODO: Move to database for production
_users: dict[str, User] = {}


def create_default_user():
    """Create a default user if none exists."""
    if not _users:
        # Default credentials: username=admin@example.com, password=admin
        # Change these in production!
        _users["admin@example.com"] = User(
            username="admin@example.com", hashed_password=get_password_hash("admin")
        )


def get_user(username: str) -> Optional[User]:
    """Get user by username."""
    return _users.get(username)


def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(username: str, password: str) -> User:
    """Create a new user."""
    if username in _users:
        raise ValueError(f"User {username} already exists")

    user = User(username=username, hashed_password=get_password_hash(password))
    _users[username] = user
    return user


# Initialize default user on module load
create_default_user()
