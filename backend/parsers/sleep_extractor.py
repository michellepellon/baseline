"""
Sleep-specific data extraction from HealthKit XML.
"""

from pathlib import Path

import polars as pl

from backend.parsers.healthkit_xml import HealthKitXMLParser


class SleepExtractor:
    """Extract and process sleep analysis data from HealthKit."""

    SLEEP_TYPE = "HKCategoryTypeIdentifierSleepAnalysis"

    # Sleep stage value mappings
    SLEEP_STAGES = {
        "HKCategoryValueSleepAnalysisInBed": "in_bed",
        "HKCategoryValueSleepAnalysisAsleepUnspecified": "asleep_unspecified",
        "HKCategoryValueSleepAnalysisAwake": "awake",
        "HKCategoryValueSleepAnalysisAsleepCore": "asleep_core",
        "HKCategoryValueSleepAnalysisAsleepDeep": "asleep_deep",
        "HKCategoryValueSleepAnalysisAsleepREM": "asleep_rem",
    }

    def __init__(self, xml_path: str | Path):
        """
        Initialize extractor with path to export.xml file.

        Args:
            xml_path: Path to the HealthKit export.xml file
        """
        self.parser = HealthKitXMLParser(xml_path)

    def extract_sleep_data(self) -> pl.DataFrame:
        """
        Extract all sleep analysis records.

        Returns:
            Polars DataFrame with sleep data including normalized stage names
        """
        df = self.parser.parse_records(record_type=self.SLEEP_TYPE)

        if df.is_empty():
            return df

        # Add normalized sleep stage column
        df = df.with_columns(
            pl.col("value")
            .replace(self.SLEEP_STAGES, default="unknown")
            .alias("sleep_stage")
        )

        # Calculate duration in minutes
        df = df.with_columns(
            (
                (pl.col("endDate") - pl.col("startDate"))
                .dt.total_minutes()
                .alias("duration_minutes")
            )
        )

        # Add date column for grouping by night
        df = df.with_columns(pl.col("startDate").dt.date().alias("date"))

        return df

    def get_sleep_stages_summary(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Summarize sleep stages by night.

        Args:
            df: DataFrame from extract_sleep_data()

        Returns:
            DataFrame with summary statistics per night
        """
        if df.is_empty():
            return df

        summary = (
            df.group_by("date", "sleep_stage")
            .agg(
                [
                    pl.col("duration_minutes").sum().alias("total_minutes"),
                    pl.col("startDate").min().alias("first_event"),
                    pl.col("endDate").max().alias("last_event"),
                ]
            )
            .sort("date", "sleep_stage")
        )

        return summary

    def get_nightly_totals(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Calculate total sleep metrics per night.

        Args:
            df: DataFrame from extract_sleep_data()

        Returns:
            DataFrame with nightly totals
        """
        if df.is_empty():
            return df

        # Filter for actual sleep stages (exclude in_bed)
        sleep_df = df.filter(
            pl.col("sleep_stage").is_in(
                ["asleep_core", "asleep_deep", "asleep_rem", "asleep_unspecified"]
            )
        )

        nightly = (
            sleep_df.group_by("date")
            .agg(
                [
                    pl.col("startDate").min().alias("sleep_start"),
                    pl.col("endDate").max().alias("sleep_end"),
                    pl.col("duration_minutes").sum().alias("total_sleep_minutes"),
                    pl.col("sourceName").first().alias("source"),
                ]
            )
            .with_columns(
                [
                    (pl.col("total_sleep_minutes") / 60).alias("total_sleep_hours"),
                    (
                        (pl.col("sleep_end") - pl.col("sleep_start"))
                        .dt.total_minutes()
                        .alias("time_in_bed_minutes")
                    ),
                ]
            )
            .with_columns(
                [
                    (
                        (pl.col("total_sleep_minutes") / pl.col("time_in_bed_minutes"))
                        * 100
                    ).alias("sleep_efficiency_pct")
                ]
            )
            .sort("date")
        )

        return nightly
