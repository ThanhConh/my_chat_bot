# tiep den xu ly data lon thanh cac file json nho hon chua cac table item
import json
import logging
from pathlib import Path # chuyen tu str sang duong dan 
from core.settings_loader import load_settings

from core.setup_logging import setup_logging

setup_logging()
settings = load_settings()

logger = logging.getLogger("ingestion")

INPUT_PATH = Path(settings["data"]["raw_dir"]) # str
OUTPUT_PATH = Path(settings["data"]["processed_dir"]) # str

def load_data():
    # mo file json
    file_path = INPUT_PATH / "database_export_2026-01-23T02-02-46.json"

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Loaded {len(data)} records from {file_path}")
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        return []
    
    tables = data.get("tables", [])

    for table_name, table_data in tables.items():
        if not table_data:
            logger.warning(f"Table {table_name} is empty")
            continue

        logger.info(f"Processing table: {table_name} with {len(table_data)} rows")
        output_file = OUTPUT_PATH / f"{table_name}.json"
        
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(table_data, file, ensure_ascii=False, indent=4)

        logger.info(f"Saved table: {table_name} to {output_file}")

if __name__ == "__main__":
    load_data()