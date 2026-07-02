import json 
import logging
from pathlib import Path

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_interior_styles():
    file_path = Path(settings["data"]["processed_dir"] / "interiorStyles.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            interior_styles = json.load(file)
            logger.info(f"Loaded {len(interior_styles)} interior styles from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    if isinstance(interior_styles, dict):
        interior_styles = list(interior.values())

    if not isinstance(interior_styles, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(architecture_types)}")
        return []

    if not interior_styles:
        logger.warning(f"No interior styles found in {file_path}")
        return []
        
    chunks = []

    for idx, interior_style in enumerate(interior_styles):
        if not isinstance(interior_style, dict):
            logger.warning(f"Invalid interior style data at index {idx}: {interior_style}")
            continue

        interior_id = interior_style.get("id", "")
        interior_name = interior_style.get("name", "")
        interior_slug = interior_style.get("slug", "")
        interior_description = interior_style.get("description")
        interior_image_url = interior_style.get("imageUrl", "")
        
        
        if not interior_name:
            logger.warning(f"Interior style at index {idx} has no name")
            continue

        if not interior_slug:
            logger.warning(f"Interior style at index {idx} has no slug")
            continue

        if not interior_description:
            logger.warning(f"Interior style at index {idx} has no description")
            continue

        if not interior_image_url:
            logger.warning(f"Interior style at index {idx} has no image url")
            continue

        
        text_parts = [
            f"Loại kiến trúc: {interior_name}",
            f"Hình ảnh minh họa: {interior_name} : {interior_image_url}",
        ]

        chunks.append({
            "text": "\n".join(text_parts),
            "metadata": {
                "type": "interiorStyle",
                "source": "interiorStyles.json",
                "interior_id": interior_id,
                "interior_name": interior_name,
                "interior_slug": interior_slug,
                "interior_description": interior_description,
                "interior_image_url": interior_image_url,
            },
        })
    
    if not chunks:
        logger.warning("No chunks generated")
        return []

    logger.info(f"Successfully generated {len(chunks)} chunks from interior styles")
    return chunks   