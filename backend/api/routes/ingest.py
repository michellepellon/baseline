"""
Data ingestion endpoints for uploading and processing HealthKit XML files.
"""

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from backend.api.routes.auth import get_current_user
from backend.database.sleep_db import SleepDatabase
from backend.parsers.sleep_extractor import SleepExtractor

router = APIRouter(prefix="/api", tags=["ingest"])


@router.post("/ingest")
async def ingest_healthkit_xml(
    current_user: Annotated[str, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    """
    Upload and process a HealthKit export.xml file.

    Extracts sleep data and stores it in the database.

    Args:
        file: HealthKit export.xml file

    Returns:
        Summary of ingested data including record counts
    """
    if not file.filename.endswith('.xml'):
        raise HTTPException(
            status_code=400,
            detail="File must be an XML file"
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        extractor = SleepExtractor(tmp_path)
        sleep_df = extractor.extract_sleep_data()

        if sleep_df.is_empty():
            raise HTTPException(
                status_code=400,
                detail="No sleep data found in the uploaded file"
            )

        nightly_df = extractor.get_nightly_totals(sleep_df)

        with SleepDatabase() as db:
            records_inserted = db.insert_sleep_records(sleep_df)
            summaries_inserted = db.insert_nightly_summary(nightly_df)
            db.update_sleep_stage_percentages()

        Path(tmp_path).unlink()

        return {
            "message": "Data ingested successfully",
            "records": records_inserted,
            "summaries": summaries_inserted,
            "nights": len(nightly_df),
            "date_range": {
                "start": str(nightly_df["date"].min()),
                "end": str(nightly_df["date"].max())
            }
        }

    except Exception as e:
        if 'tmp_path' in locals():
            Path(tmp_path).unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(e))
