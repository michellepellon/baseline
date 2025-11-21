"""
Health insights generation using Ollama LLM.
"""

import os
from datetime import datetime, timedelta
from typing import Annotated

import ollama
from fastapi import APIRouter, Depends, HTTPException

from backend.api.routes.auth import get_current_user
from backend.database.sleep_db import SleepDatabase

router = APIRouter(prefix="/api/insights", tags=["insights"])


def _format_sleep_data_for_prompt(summary_df) -> str:
    """
    Format sleep data for LLM consumption.

    Args:
        summary_df: Polars DataFrame with nightly summary data

    Returns:
        Formatted string with sleep data
    """
    if summary_df.is_empty():
        return "No sleep data available."

    lines = []
    for row in summary_df.iter_rows(named=True):
        date = row["date"]
        sleep_hours = row["total_sleep_hours"]
        efficiency = row["sleep_efficiency_pct"]

        line = f"- {date}: {sleep_hours:.1f} hours, {efficiency:.0f}% efficiency"

        # Add sleep stage data if available
        if row.get("asleep_rem_pct"):
            rem = row["asleep_rem_pct"]
            deep = row["asleep_deep_pct"]
            core = row["asleep_core_pct"]
            line += f" (REM: {rem:.0f}%, Deep: {deep:.0f}%, Core: {core:.0f}%)"

        lines.append(line)

    return "\n".join(lines)


def _get_benchmarks_text(db: SleepDatabase) -> str:
    """
    Get sleep benchmarks for context.

    Args:
        db: Active SleepDatabase connection

    Returns:
        Formatted string with benchmark data
    """
    result = db.conn.execute(
        "SELECT metric_name, optimal_min, optimal_max, description FROM sleep_benchmarks"
    ).fetchall()

    if not result:
        return "No benchmark data available."

    lines = []
    for row in result:
        metric, min_val, max_val, desc = row
        lines.append(f"- {metric}: {min_val}-{max_val} ({desc})")

    return "\n".join(lines)


@router.get("/generate")
async def generate_insights(
    current_user: Annotated[str, Depends(get_current_user)],
    days: int = 7,
    force_regenerate: bool = False
):
    """
    Generate health insights based on recent sleep data.

    Args:
        current_user: Authenticated user
        days: Number of days to analyze (default 7)
        force_regenerate: Force regeneration even if cached insights exist

    Returns:
        Generated insights and recommendations
    """
    with SleepDatabase() as db:
        # Check for cached insights unless force_regenerate is True
        if not force_regenerate:
            cached = db.conn.execute(
                """
                SELECT insights_text, stats, generated_at
                FROM insights_cache
                WHERE days_analyzed = ?
                AND generated_at > now() - INTERVAL '7 days'
                ORDER BY generated_at DESC
                LIMIT 1
                """,
                [days]
            ).fetchone()

            if cached:
                import json
                # Parse cached JSON
                insights_data = json.loads(cached[0]) if isinstance(cached[0], str) else cached[0]
                stats_data = json.loads(cached[1]) if isinstance(cached[1], str) else cached[1]

                return {
                    "insights": insights_data,
                    "stats": stats_data,
                    "generated_at": cached[2].isoformat(),
                    "from_cache": True
                }

        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        # Fetch sleep data
        summary_df = db.get_nightly_summary(
            start_date=str(start_date),
            end_date=str(end_date)
        )

        if summary_df.is_empty():
            raise HTTPException(
                status_code=404,
                detail="No sleep data available for the requested period"
            )

        # Format data for LLM
        sleep_data = _format_sleep_data_for_prompt(summary_df)
        benchmarks = _get_benchmarks_text(db)

        # Build prompt
        prompt = f"""You are a health insights assistant that analyzes consumer sleep and cardiac data.
You are not a doctor and you do not provide diagnoses. You provide clear, practical guidance to help users improve their sleep habits.

INPUTS

HEALTH BENCHMARKS
{benchmarks}

USER DATA (LAST {days} DAYS)
{sleep_data}

TASK

Using ONLY the data provided above:

1. Give a brief summary (2-3 sentences) of the user's overall sleep quality and key trends.
2. Provide 2-3 specific, actionable recommendations to improve sleep (focus on behaviors the user can realistically change).
3. Highlight any patterns that may be concerning and explain why they warrant attention. If appropriate, suggest when the user should consider discussing this with a clinician.

STYLE & CONSTRAINTS

- Keep the response concise: maximum 3-4 short paragraphs.
- Use a warm, supportive, and professional tone.
- Base all comments on established, evidence-informed sleep hygiene principles (e.g., consistent schedule, light exposure, caffeine timing, exercise, etc.).
- Avoid medical jargon where possible; briefly explain any necessary technical terms.
- Do NOT speculate beyond the data or make definitive medical claims or diagnoses.

OUTPUT FORMAT

You MUST respond with valid JSON in this exact structure (no additional text before or after):

{{
  "overview": "1 short paragraph (2-3 sentences) summarizing sleep quality and main patterns",
  "recommendations": [
    "First specific, actionable recommendation",
    "Second specific, actionable recommendation",
    "Third specific, actionable recommendation (optional)"
  ],
  "patterns": "1 short paragraph explaining any concerning trends and suggested next steps, or 'No significant concerns identified' if data looks good"
}}"""

        # Get Ollama host from environment
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

        try:
            # Generate insights using Ollama
            client = ollama.Client(host=ollama_host)

            # Use a small, fast model for quick responses
            # llama3.2 is a good balance of speed and quality
            response = client.generate(
                model="llama3.2",
                prompt=prompt,
            )

            insights_text = response["response"]

            # Parse JSON response
            import json
            try:
                # Try to parse the JSON response
                insights_json = json.loads(insights_text)

                # Validate structure
                if not all(k in insights_json for k in ["overview", "recommendations", "patterns"]):
                    raise ValueError("Invalid JSON structure from LLM")

            except (json.JSONDecodeError, ValueError) as e:
                # If JSON parsing fails, fall back to plain text format
                insights_json = {
                    "overview": insights_text,
                    "recommendations": [],
                    "patterns": ""
                }

            # Calculate basic statistics for context
            stats = {
                "average_sleep_hours": float(summary_df["total_sleep_hours"].mean()),
                "average_efficiency": float(summary_df["sleep_efficiency_pct"].mean()),
                "nights_analyzed": len(summary_df),
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

            # Cache the insights (store as JSON string)
            db.conn.execute(
                """
                INSERT INTO insights_cache (days_analyzed, insights_text, stats, generated_at)
                VALUES (?, ?, ?, now())
                """,
                [days, json.dumps(insights_json), json.dumps(stats)]
            )

            return {
                "insights": insights_json,
                "stats": stats,
                "generated_at": datetime.now().isoformat(),
                "from_cache": False
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate insights: {str(e)}"
            )
