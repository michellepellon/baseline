"""
DuckDB database operations for sleep data.
"""

from pathlib import Path

import duckdb
import polars as pl


class SleepDatabase:
    """Manage sleep data in DuckDB."""

    def __init__(self, db_path: str | Path = "data/sleep_analysis.duckdb"):
        """
        Initialize database connection.

        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._initialize_schema()

    def _initialize_schema(self):
        """Create tables if they don't exist."""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path) as f:
            schema_sql = f.read()
        self.conn.execute(schema_sql)

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
            )
            UPDATE sleep_nightly_summary
            SET
                asleep_core_minutes = stage_totals.core_min,
                asleep_deep_minutes = stage_totals.deep_min,
                asleep_rem_minutes = stage_totals.rem_min,
                awake_minutes = stage_totals.awake_min,
                asleep_core_pct = (stage_totals.core_min::DOUBLE
                    / total_sleep_minutes * 100),
                asleep_deep_pct = (stage_totals.deep_min::DOUBLE
                    / total_sleep_minutes * 100),
                asleep_rem_pct = (stage_totals.rem_min::DOUBLE
                    / total_sleep_minutes * 100),
                awake_pct = (stage_totals.awake_min::DOUBLE
                    / time_in_bed_minutes * 100),
                updated_at = now()
            FROM stage_totals
            WHERE sleep_nightly_summary.date = stage_totals.date
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

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
