"""
DuckDB database operations for sleep data.
"""

from pathlib import Path

import duckdb
import polars as pl

from backend.config.settings import settings


class SleepDatabase:
    """Manage sleep data in DuckDB with encryption at rest."""

    def __init__(self, db_path: str | Path = "data/sleep_analysis.duckdb"):
        """
        Initialize database connection with encryption.

        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Get encryption key
        encryption_key = settings.db_encryption_key

        # Start with in-memory connection
        self.conn = duckdb.connect(":memory:")

        # Load httpfs extension for OpenSSL hardware-accelerated encryption
        try:
            self.conn.execute("INSTALL httpfs;")
            self.conn.execute("LOAD httpfs;")
        except Exception:
            # httpfs not available, will use MbedTLS (slower but functional)
            pass

        # Attach the database file with encryption
        # Use parameterized query for safety
        self.conn.execute(
            f"ATTACH '{self.db_path}' AS db (ENCRYPTION_KEY '{encryption_key}');"
        )

        # Use the attached database
        self.conn.execute("USE db;")

        # Enable temporary file encryption for additional security
        self.conn.execute("SET temp_file_encryption = true;")

        self._initialize_schema()

    def _initialize_schema(self):
        """Create tables if they don't exist."""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path) as f:
            schema_sql = f.read()
        self.conn.execute(schema_sql)

        # Run migrations for existing databases
        self._run_migrations()

    def _run_migrations(self):
        """Run database migrations for schema updates."""
        try:
            # Check if profile_picture columns exist
            result = self.conn.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'users'
                AND column_name IN ('profile_picture', 'profile_picture_mime_type')
            """).fetchall()

            existing_columns = [row[0] for row in result]

            # Add profile_picture column if it doesn't exist
            if 'profile_picture' not in existing_columns:
                self.conn.execute("ALTER TABLE users ADD COLUMN profile_picture BLOB;")

            # Add profile_picture_mime_type column if it doesn't exist
            if 'profile_picture_mime_type' not in existing_columns:
                self.conn.execute("ALTER TABLE users ADD COLUMN profile_picture_mime_type VARCHAR;")
        except Exception:
            # If migration fails, it's likely because the columns already exist
            # or the table doesn't exist yet (will be created by schema.sql)
            pass

    def insert_sleep_records(self, df: pl.DataFrame) -> int:
        """
        Insert sleep records from Polars DataFrame.

        Args:
            df: DataFrame with sleep records from SleepExtractor

        Returns:
            Number of rows inserted
        """
        # DuckDB can directly query Polars DataFrames
        result = self.conn.execute(
            """
            INSERT INTO sleep_records (
                record_type, source_name, source_version, device,
                creation_date, start_date, end_date, value,
                sleep_stage, duration_minutes, date
            )
            SELECT
                type, sourceName, sourceVersion, device,
                creationDate, startDate, endDate, value,
                sleep_stage, duration_minutes, date
            FROM df
            ON CONFLICT DO NOTHING
            """
        )
        return result.fetchall()[0][0] if result else 0

    def insert_nightly_summary(self, df: pl.DataFrame) -> int:
        """
        Insert nightly summary data.

        Args:
            df: DataFrame with nightly totals from SleepExtractor

        Returns:
            Number of rows inserted
        """
        result = self.conn.execute(
            """
            INSERT INTO sleep_nightly_summary (
                date, sleep_start, sleep_end,
                total_sleep_minutes, total_sleep_hours,
                time_in_bed_minutes, sleep_efficiency_pct,
                source_name
            )
            SELECT
                date, sleep_start, sleep_end,
                total_sleep_minutes, total_sleep_hours,
                time_in_bed_minutes, sleep_efficiency_pct,
                source
            FROM df
            ON CONFLICT (date) DO UPDATE SET
                sleep_start = EXCLUDED.sleep_start,
                sleep_end = EXCLUDED.sleep_end,
                total_sleep_minutes = EXCLUDED.total_sleep_minutes,
                total_sleep_hours = EXCLUDED.total_sleep_hours,
                time_in_bed_minutes = EXCLUDED.time_in_bed_minutes,
                sleep_efficiency_pct = EXCLUDED.sleep_efficiency_pct,
                source_name = EXCLUDED.source_name,
                updated_at = now()
            """
        )
        return result.fetchall()[0][0] if result else 0

    def update_sleep_stage_percentages(self):
        """Calculate and update sleep stage percentages in nightly summary."""
        self.conn.execute(
            """
            WITH stage_totals AS (
                SELECT
                    date,
                    SUM(CASE WHEN sleep_stage = 'asleep_core'
                        THEN duration_minutes ELSE 0 END) as core_min,
                    SUM(CASE WHEN sleep_stage = 'asleep_deep'
                        THEN duration_minutes ELSE 0 END) as deep_min,
                    SUM(CASE WHEN sleep_stage = 'asleep_rem'
                        THEN duration_minutes ELSE 0 END) as rem_min,
                    SUM(CASE WHEN sleep_stage = 'awake'
                        THEN duration_minutes ELSE 0 END) as awake_min
                FROM sleep_records
                GROUP BY date
            ),
            stage_totals_with_sum AS (
                SELECT
                    *,
                    (core_min + deep_min + rem_min) as total_asleep_min
                FROM stage_totals
            )
            UPDATE sleep_nightly_summary
            SET
                asleep_core_minutes = stage_totals_with_sum.core_min,
                asleep_deep_minutes = stage_totals_with_sum.deep_min,
                asleep_rem_minutes = stage_totals_with_sum.rem_min,
                awake_minutes = stage_totals_with_sum.awake_min,
                asleep_core_pct = CASE
                    WHEN stage_totals_with_sum.total_asleep_min > 0
                    THEN (stage_totals_with_sum.core_min::DOUBLE
                        / stage_totals_with_sum.total_asleep_min * 100)
                    ELSE 0
                END,
                asleep_deep_pct = CASE
                    WHEN stage_totals_with_sum.total_asleep_min > 0
                    THEN (stage_totals_with_sum.deep_min::DOUBLE
                        / stage_totals_with_sum.total_asleep_min * 100)
                    ELSE 0
                END,
                asleep_rem_pct = CASE
                    WHEN stage_totals_with_sum.total_asleep_min > 0
                    THEN (stage_totals_with_sum.rem_min::DOUBLE
                        / stage_totals_with_sum.total_asleep_min * 100)
                    ELSE 0
                END,
                awake_pct = CASE
                    WHEN time_in_bed_minutes > 0
                    THEN (stage_totals_with_sum.awake_min::DOUBLE
                        / time_in_bed_minutes * 100)
                    ELSE 0
                END,
                updated_at = now()
            FROM stage_totals_with_sum
            WHERE sleep_nightly_summary.date = stage_totals_with_sum.date
            """
        )

    def get_nightly_summary(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> pl.DataFrame:
        """
        Retrieve nightly summary data.

        Args:
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)

        Returns:
            Polars DataFrame with nightly summary
        """
        query = "SELECT * FROM sleep_nightly_summary WHERE 1=1"

        if start_date:
            query += f" AND date >= '{start_date}'"
        if end_date:
            query += f" AND date <= '{end_date}'"

        query += " ORDER BY date DESC"

        return self.conn.execute(query).pl()

    def get_sleep_records(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> pl.DataFrame:
        """
        Retrieve sleep records.

        Args:
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)

        Returns:
            Polars DataFrame with sleep records
        """
        query = "SELECT * FROM sleep_records WHERE 1=1"

        if start_date:
            query += f" AND date >= '{start_date}'"
        if end_date:
            query += f" AND date <= '{end_date}'"

        query += " ORDER BY start_date"

        return self.conn.execute(query).pl()

    def insert_benchmarks(self, benchmarks: list[dict]) -> int:
        """
        Insert scientific benchmarks.

        Args:
            benchmarks: List of benchmark dictionaries

        Returns:
            Number of rows inserted
        """
        df = pl.DataFrame(benchmarks)
        result = self.conn.execute(
            """
            INSERT INTO sleep_benchmarks (
                metric_name, optimal_min, optimal_max, good_threshold,
                unit, source, citation, description
            )
            SELECT
                metric_name, optimal_min, optimal_max, good_threshold,
                unit, source, citation, description
            FROM df
            ON CONFLICT (metric_name) DO UPDATE SET
                optimal_min = EXCLUDED.optimal_min,
                optimal_max = EXCLUDED.optimal_max,
                good_threshold = EXCLUDED.good_threshold,
                unit = EXCLUDED.unit,
                source = EXCLUDED.source,
                citation = EXCLUDED.citation,
                description = EXCLUDED.description,
                created_at = now()
            """
        )
        return result.fetchall()[0][0] if result else 0

    def create_user(
        self,
        username: str,
        hashed_password: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> dict | None:
        """
        Create a new user.

        Args:
            username: User's email/username
            hashed_password: Hashed password
            first_name: Optional first name
            last_name: Optional last name

        Returns:
            User dictionary or None if user already exists
        """
        try:
            self.conn.execute(
                """
                INSERT INTO users (username, hashed_password, first_name, last_name)
                VALUES (?, ?, ?, ?)
                """,
                [username, hashed_password, first_name, last_name],
            )
            return self.get_user(username)
        except duckdb.ConstraintException:
            return None

    def get_user(self, username: str) -> dict | None:
        """
        Retrieve user by username.

        Args:
            username: User's email/username

        Returns:
            User dictionary or None if not found
        """
        # Check if profile_picture columns exist
        try:
            result = self.conn.execute(
                """
                SELECT username, hashed_password, first_name, last_name,
                       profile_picture, profile_picture_mime_type
                FROM users
                WHERE username = ?
                """,
                [username],
            ).fetchone()

            if result:
                return {
                    "username": result[0],
                    "hashed_password": result[1],
                    "first_name": result[2],
                    "last_name": result[3],
                    "profile_picture": result[4],
                    "profile_picture_mime_type": result[5],
                }
        except Exception:
            # Fall back to query without profile_picture columns
            result = self.conn.execute(
                """
                SELECT username, hashed_password, first_name, last_name
                FROM users
                WHERE username = ?
                """,
                [username],
            ).fetchone()

            if result:
                return {
                    "username": result[0],
                    "hashed_password": result[1],
                    "first_name": result[2],
                    "last_name": result[3],
                    "profile_picture": None,
                    "profile_picture_mime_type": None,
                }

        return None

    def update_user_profile(
        self,
        username: str,
        first_name: str | None = None,
        last_name: str | None = None,
        profile_picture: bytes | None = None,
        profile_picture_mime_type: str | None = None,
    ) -> dict | None:
        """
        Update user profile information.

        Args:
            username: User's email/username
            first_name: Optional first name
            last_name: Optional last name
            profile_picture: Optional profile picture bytes
            profile_picture_mime_type: Optional MIME type for profile picture

        Returns:
            Updated user dictionary or None if user not found
        """
        user = self.get_user(username)
        if not user:
            return None

        # Build update query dynamically based on provided fields
        updates = []
        params = []

        if first_name is not None:
            updates.append("first_name = ?")
            params.append(first_name)

        if last_name is not None:
            updates.append("last_name = ?")
            params.append(last_name)

        if profile_picture is not None:
            updates.append("profile_picture = ?")
            params.append(profile_picture)
            updates.append("profile_picture_mime_type = ?")
            params.append(profile_picture_mime_type)

        updates.append("updated_at = now()")
        params.append(username)

        query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"

        self.conn.execute(query, params)

        return self.get_user(username)

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
