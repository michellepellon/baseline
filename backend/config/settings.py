"""
Application configuration and settings management.
"""

import os
import secrets
from pathlib import Path


class Settings:
    """Application settings with encryption key management."""

    def __init__(self):
        # Database encryption key
        # In production, this should be stored in a secure vault (e.g., AWS Secrets Manager, HashiCorp Vault)
        # For development, use environment variable or generate a persistent key
        self.db_encryption_key = self._get_or_create_encryption_key()

        # Database path
        self.db_path = Path(os.getenv("DB_PATH", "data/sleep_analysis.duckdb"))

    def _get_or_create_encryption_key(self) -> str:
        """
        Get encryption key from environment or create a persistent one.

        The key is stored in a .key file for persistence across restarts.
        In production, use a proper secrets management system.

        Returns:
            Base64-encoded 32-byte encryption key
        """
        # First, check environment variable
        env_key = os.getenv("DUCKDB_ENCRYPTION_KEY")
        if env_key:
            return env_key

        # Second, check for persistent key file
        key_file = Path("data/.db_encryption.key")
        if key_file.exists():
            return key_file.read_text().strip()

        # Third, generate a new key and persist it
        # Generate a cryptographically secure 32-byte key
        key_bytes = secrets.token_bytes(32)
        # Encode as base64 for easier handling
        import base64

        key_b64 = base64.b64encode(key_bytes).decode("ascii")

        # Persist the key
        key_file.parent.mkdir(parents=True, exist_ok=True)
        key_file.write_text(key_b64)
        # Set restrictive permissions (owner read/write only)
        key_file.chmod(0o600)

        return key_b64


# Global settings instance
settings = Settings()
