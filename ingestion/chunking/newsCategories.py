import json 
import logging
from pathlib import Path

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_news_categories():
    file_path = Path(settings["data"]["processed_dir"] / "newsCategories.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            news_categories = json.load(file)
            logger.info(f"Loaded {len(news_categories)} news categories from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    if isinstance(news_categories, dict):
        news_categories = list(news_categories.values())

    if not isinstance(news_categories, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(news_categories)}")
        return []

    if not news_categories:
        logger.warning(f"No news categories found in {file_path}")
        return []
        
    chunks = []
    for idx, category in enumerate(news_categories):
        if not isinstance(category, dict):
            logger.warning(f"Invalid news category data at index {idx}: {category}")
            continue

        category_id = category.get("id", "")
        category_name = category.get("name", "")
        category_slug = category.get("slug", "")
        category_description = category.get("description")
        
        if not category_name:
            logger.warning(f"News category at index {idx} has no name")
            continue
  
        text_parts = [
            f"Loại tin tức: {category_name}",
        ]

        chunks.append({
            "text": "\n".join(text_parts),
            "metadata": {
                "type": "newsCategory",
                "source": "newsCategories.json",
                "category_id": category_id,
                "category_name": category_name,
                "category_slug": category_slug,
                "category_description": category_description,
                "category_image_url": category_image_url,
            },
        })
    
    if not chunks:
        logger.warning("No chunks generated")
        return []

    logger.info(f"Successfully generated {len(chunks)} chunks from news categories")
    return chunks   