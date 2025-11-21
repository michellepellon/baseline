"""
HealthKit XML parser using xml.etree.ElementTree and Polars.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import polars as pl


class HealthKitXMLParser:
    """Parser for Apple HealthKit export.xml files."""

    def __init__(self, xml_path: str | Path):
        """
        Initialize parser with path to export.xml file.

        Args:
            xml_path: Path to the HealthKit export.xml file
        """
        self.xml_path = Path(xml_path)
        if not self.xml_path.exists():
            raise FileNotFoundError(f"File not found: {self.xml_path}")

    def parse_records(self, record_type: str | None = None) -> pl.DataFrame:
        """
        Parse Record elements from the XML file.

        Args:
            record_type: Optional filter for specific record type
                        (e.g., 'HKCategoryTypeIdentifierSleepAnalysis')

        Returns:
            Polars DataFrame with record data
        """
        records = []

        # Use iterparse for memory efficiency with large files
        context = ET.iterparse(self.xml_path, events=("start", "end"))
        _, root = next(context)

        for event, elem in context:
            if event == "end" and elem.tag == "Record":
                # Filter by record type if specified
                if record_type is None or elem.get("type") == record_type:
                    record = {
                        "type": elem.get("type"),
                        "sourceName": elem.get("sourceName"),
                        "sourceVersion": elem.get("sourceVersion"),
                        "device": elem.get("device"),
                        "unit": elem.get("unit"),
                        "creationDate": elem.get("creationDate"),
                        "startDate": elem.get("startDate"),
                        "endDate": elem.get("endDate"),
                        "value": elem.get("value"),
                    }
                    records.append(record)

                # Clear element to free memory
                elem.clear()
                root.clear()

        if not records:
            return pl.DataFrame()

        # Create Polars DataFrame
        df = pl.DataFrame(records)

        # Parse dates to datetime
        date_columns = ["creationDate", "startDate", "endDate"]
        for col in date_columns:
            if col in df.columns:
                df = df.with_columns(
                    pl.col(col).str.strptime(
                        pl.Datetime,
                        "%Y-%m-%d %H:%M:%S %z",
                        strict=False,
                    )
                )

        return df

    def get_export_date(self) -> datetime:
        """
        Extract the export date from the XML file.

        Returns:
            Export date as datetime object
        """
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        export_date_elem = root.find("ExportDate")

        if export_date_elem is not None:
            date_str = export_date_elem.get("value")
            return datetime.fromisoformat(date_str)

        raise ValueError("Export date not found in XML file")

    def get_me_data(self) -> dict[str, str]:
        """
        Extract personal data from the Me element.

        Returns:
            Dictionary with personal health data
        """
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        me_elem = root.find("Me")

        if me_elem is not None:
            return dict(me_elem.attrib)

        return {}
