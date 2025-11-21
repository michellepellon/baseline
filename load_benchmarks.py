"""
Load scientific benchmarks from TOML configuration into the database.
"""

import tomllib
from pathlib import Path

from backend.database.sleep_db import SleepDatabase


def load_benchmarks_from_toml(toml_path: str | Path):
    """
    Load benchmarks from TOML file and insert into database.

    Args:
        toml_path: Path to the sleep_science_config.toml file
    """
    with open(toml_path, "rb") as f:
        config = tomllib.load(f)

    benchmarks = []

    # Extract metrics from the config
    metrics = config.get("metrics", {})

    for metric_name, metric_data in metrics.items():
        benchmark = {
            "metric_name": metric_name,
            "optimal_min": metric_data.get("optimal_min_hours")
            or metric_data.get("target_percentage_min")
            or metric_data.get("optimal_start_hour")
            or metric_data.get("optimal_max_minutes"),
            "optimal_max": metric_data.get("optimal_max_hours")
            or metric_data.get("target_percentage_max")
            or metric_data.get("optimal_end_hour"),
            "good_threshold": metric_data.get("good_threshold_hours")
            or metric_data.get("good_threshold")
            or metric_data.get("optimal_threshold")
            or metric_data.get("good_max_minutes")
            or metric_data.get("good_variability_minutes"),
            "unit": metric_data.get("unit", ""),
            "source": metric_data.get("source", ""),
            "citation": metric_data.get("citation", ""),
            "description": metric_data.get("description", ""),
        }

        # Clean up None values
        benchmark = {k: v for k, v in benchmark.items() if v is not None}
        benchmarks.append(benchmark)

    # Insert into database
    with SleepDatabase() as db:
        inserted = db.insert_benchmarks(benchmarks)
        print(f"Inserted {inserted} benchmarks into database")

    return benchmarks


if __name__ == "__main__":
    config_path = Path("backend/config/sleep_science_config.toml")

    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        exit(1)

    print(f"Loading benchmarks from {config_path}...")
    benchmarks = load_benchmarks_from_toml(config_path)

    print(f"\nLoaded {len(benchmarks)} benchmarks:")
    for b in benchmarks:
        print(f"  - {b['metric_name']}: {b.get('description', 'No description')}")

    print("\nBenchmarks successfully loaded into database!")
