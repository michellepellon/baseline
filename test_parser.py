"""Test the HealthKit XML parser."""

from backend.parsers.sleep_extractor import SleepExtractor

# Test with the sample export
extractor = SleepExtractor("test_export/export.xml")

print("Extracting sleep data...")
sleep_df = extractor.extract_sleep_data()
print(f"Total sleep records: {len(sleep_df)}")
print("\nFirst few records:")
print(sleep_df.head())

print("\n\nSleep stages summary:")
summary = extractor.get_sleep_stages_summary(sleep_df)
print(summary.head(10))

print("\n\nNightly totals:")
nightly = extractor.get_nightly_totals(sleep_df)
print(nightly.head())
