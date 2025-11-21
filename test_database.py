"""Test the DuckDB integration."""

from backend.database.sleep_db import SleepDatabase
from backend.parsers.sleep_extractor import SleepExtractor

print("Extracting sleep data...")
extractor = SleepExtractor("test_export/export.xml")
sleep_df = extractor.extract_sleep_data()
nightly_df = extractor.get_nightly_totals(sleep_df)

print(f"Extracted {len(sleep_df)} sleep records")
print(f"Extracted {len(nightly_df)} nightly summaries")

print("\nInitializing database...")
with SleepDatabase() as db:
    print("Inserting sleep records...")
    records_inserted = db.insert_sleep_records(sleep_df)
    print(f"Inserted {records_inserted} sleep records")

    print("Inserting nightly summaries...")
    summaries_inserted = db.insert_nightly_summary(nightly_df)
    print(f"Inserted {summaries_inserted} nightly summaries")

    print("Updating sleep stage percentages...")
    db.update_sleep_stage_percentages()

    print("\nRetrieving data from database...")
    summary = db.get_nightly_summary()
    print(f"Retrieved {len(summary)} nightly summaries")
    print("\nNightly summary from database:")
    print(summary)

print("\nDatabase test complete!")
