"""
User management with DuckDB persistence.
"""

from dataclasses import dataclass
from typing import Optional

from backend.auth.security import get_password_hash, verify_password
from backend.database.sleep_db import SleepDatabase


@dataclass
class User:
    """User model."""

    username: str
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[bytes] = None
    profile_picture_mime_type: Optional[str] = None


def _get_db() -> SleepDatabase:
    """Get database connection."""
    return SleepDatabase()


def create_default_user():
    """Create a default user if none exists."""
    db = _get_db()
    try:
        existing_user = db.get_user("admin@example.com")
        if not existing_user:
            # Default credentials: username=admin@example.com, password=admin
            # Change these in production!
            db.create_user(
                username="admin@example.com",
                hashed_password=get_password_hash("admin"),
            )
    finally:
        db.close()


def get_user(username: str) -> Optional[User]:
    """Get user by username."""
    db = _get_db()
    try:
        user_dict = db.get_user(username)
        if user_dict:
            return User(
                username=user_dict["username"],
                hashed_password=user_dict["hashed_password"],
                first_name=user_dict["first_name"],
                last_name=user_dict["last_name"],
                profile_picture=user_dict.get("profile_picture"),
                profile_picture_mime_type=user_dict.get("profile_picture_mime_type"),
            )
        return None
    finally:
        db.close()


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
    db = _get_db()
    try:
        user_dict = db.create_user(
            username=username, hashed_password=get_password_hash(password)
        )
        if not user_dict:
            raise ValueError(f"User {username} already exists")

        return User(
            username=user_dict["username"],
            hashed_password=user_dict["hashed_password"],
            first_name=user_dict["first_name"],
            last_name=user_dict["last_name"],
        )
    finally:
        db.close()


def update_user_profile(
    username: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    profile_picture: Optional[bytes] = None,
    profile_picture_mime_type: Optional[str] = None,
) -> Optional[User]:
    """Update user profile information."""
    db = _get_db()
    try:
        user_dict = db.update_user_profile(
            username=username,
            first_name=first_name,
            last_name=last_name,
            profile_picture=profile_picture,
            profile_picture_mime_type=profile_picture_mime_type,
        )
        if user_dict:
            return User(
                username=user_dict["username"],
                hashed_password=user_dict["hashed_password"],
                first_name=user_dict["first_name"],
                last_name=user_dict["last_name"],
                profile_picture=user_dict.get("profile_picture"),
                profile_picture_mime_type=user_dict.get("profile_picture_mime_type"),
            )
        return None
    finally:
        db.close()


# Initialize default user on module load
create_default_user()
