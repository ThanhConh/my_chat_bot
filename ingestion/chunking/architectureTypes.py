import json 
import logging
from pathlib import Path
from core.setup_logging import setup_logging

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion.architectureTypes")

def chunk_architecture_types():
    file_path = Path(settings["data"]["processed_dir"] / "architectureTypes.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Loaded {len(data)} architecture types from {file_path}")
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        return []

    if isinstance(architecture_types, dict):
        architecture_types = list(architecture_types.values())

    if not isinstance(architecture_types, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(architecture_types)}")
        return []

    if not architecture_types:
        logger.warning(f"No architecture types found in {file_path}")
        return []
        
    chunks = []
    for idx, architecture_types in enumerate(architecture_types):
        if not isinstance(architecture_types, dict):
            logger.warning(f"Invalid architecture type data at index {idx}: {architecture_types}")
            continue

        architecture_id = architecture_types.get("id", "")
        architecture_name = architecture_types.get("name", "")
        architecture_slug = architecture_types.get("slug", "")
        architecture_description = architecture_types.get("description")
        architecture_image_url = architecture_types.get("imageUrl", "")
        
        
        if not architecture_name:
            logger.warning(f"Architecture type at index {idx} has no name")
            continue

        if not architecture_slug:
            logger.warning(f"Architecture type at index {idx} has no slug")
            continue

        if not architecture_description:
            logger.warning(f"Architecture type at index {idx} has no description")
            continue

        if not architecture_image_url:
            logger.warning(f"Architecture type at index {idx} has no image url")
            continue

        
        text_parts = [
            f"Loại kiến trúc: {architecture_name}",
            f"Hình ảnh minh họa: {architecture_name} : {architecture_image_url}",
        ]

        chunks.append({
            "text": "\n".join(text_parts),
            "metadata": {
                "type": "architectureType",
                "source": "architectureTypes.json",
                "architecture_id": architecture_id,
                "architecture_name": architecture_name,
                "architecture_slug": architecture_slug,
                "architecture_description": architecture_description,
                "architecture_image_url": architecture_image_url,
            },
        })
    
        if not chunks:
            logger.warning("No chunks generated")
            return []

    return chunks   