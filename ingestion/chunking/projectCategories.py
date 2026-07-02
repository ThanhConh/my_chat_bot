import json 
import logging
from pathlib import Path

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_project_categories():
    file_path = Path(settings["data"]["processed_dir"] / "projectCategories.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            project_categories = json.load(file)
            logger.info(f"Loaded {len(project_categories)} project categories from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    if isinstance(project_categories, dict):
        project_categories = list(project_categories.values())

    if not isinstance(project_categories, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(project_categories)}")
        return []

    if not project_categories:
        logger.warning(f"No project categories found in {file_path}")
        return []
        
    chunks = []
    for idx, project_category in enumerate(project_categories):
        if not isinstance(project_category, dict):
            logger.warning(f"Invalid project category data at index {idx}: {project_category}")
            continue

        category_id = project_category.get("id", "")
        category_name = project_category.get("name", "")
        category_slug = project_category.get("slug", "")
        category_description = project_category.get("description")
        
        if not category_name:
            logger.warning(f"Project category at index {idx} has no name")
            continue
  
        text_parts = [
            f"Loại dự án: {category_name}",
        ]

        chunks.append({
            "text": "\n".join(text_parts),
            "metadata": {
                "type": "projectCategory",
                "source": "projectCategories.json",
                "category_id": category_id,
                "category_name": category_name,
                "category_slug": category_slug,
                "category_description": category_description,
            },
        })
    
    if not chunks:
        logger.warning("No chunks generated")
        return []

    logger.info(f"Successfully generated {len(chunks)} chunks from news categories")
    return chunks   