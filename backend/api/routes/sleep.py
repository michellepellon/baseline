"""
Sleep data query endpoints.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from backend.api.routes.auth import get_current_user
from backend.database.sleep_db import SleepDatabase

router = APIRouter(prefix="/api/sleep", tags=["sleep"])


@router.get("/summary")
async def get_sleep_summary(
    current_user: Annotated[str, Depends(get_current_user)],
    start_date: Optional[str] = Query(
        None, description="Start date filter (ISO format: YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(
        None, description="End date filter (ISO format: YYYY-MM-DD)"
    )
):
    """
    Get nightly sleep summaries.

    Returns aggregated sleep metrics for each night including:
    - Total sleep duration
    - Sleep efficiency
    - Sleep stage breakdowns (REM, Deep, Core, Awake)
    - Sleep stage percentages

    Args:
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering

    Returns:
        List of nightly summary records
    """
    with SleepDatabase() as db:
        df = db.get_nightly_summary(start_date, end_date)

        if df.is_empty():
            return []

        return df.to_dicts()


@router.get("/records")
async def get_sleep_records(
    current_user: Annotated[str, Depends(get_current_user)],
    start_date: Optional[str] = Query(
        None, description="Start date filter (ISO format: YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(
        None, description="End date filter (ISO format: YYYY-MM-DD)"
    )
):
    """
    Get detailed sleep stage records.

    Returns individual sleep stage events with timestamps and durations.
    Useful for creating hypnograms and detailed visualizations.

    Args:
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering

    Returns:
        List of sleep stage records
    """
    with SleepDatabase() as db:
        df = db.get_sleep_records(start_date, end_date)

        if df.is_empty():
            return []

        return df.to_dicts()


@router.get("/stats")
async def get_sleep_stats(current_user: Annotated[str, Depends(get_current_user)]):
    """
    Get overall sleep statistics.

    Returns:
        Summary statistics across all sleep data
    """
    with SleepDatabase() as db:
        summary_df = db.get_nightly_summary()

        if summary_df.is_empty():
            return {
                "total_nights": 0,
                "average_sleep_hours": 0,
                "average_efficiency": 0
            }

        stats = {
            "total_nights": len(summary_df),
            "average_sleep_hours": float(summary_df["total_sleep_hours"].mean()),
            "average_efficiency": float(summary_df["sleep_efficiency_pct"].mean()),
            "date_range": {
                "start": str(summary_df["date"].min()),
                "end": str(summary_df["date"].max())
            }
        }

        if "asleep_rem_pct" in summary_df.columns:
            stats["average_rem_pct"] = float(
                summary_df["asleep_rem_pct"].drop_nulls().mean()
            )
            stats["average_deep_pct"] = float(
                summary_df["asleep_deep_pct"].drop_nulls().mean()
            )
            stats["average_core_pct"] = float(
                summary_df["asleep_core_pct"].drop_nulls().mean()
            )

        return stats
