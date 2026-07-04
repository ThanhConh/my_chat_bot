import json
import logging
from pathlib import Path

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_hero_slides():
    file_path = Path(settings["data"]["processed_dir"] / "heroSlides.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    # đọc file heroSlides.json
    try:
        with open(file_path, encoding="utf-8") as file:
            hero_slides = json.load(file) # load file = đọc file
            logger.info(f"Loaded {len(hero_slides)} records from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    # kiểm tra có phải là dict hay không nếu đúng chuyển sang list
    if isinstance(hero_slides, dict):
        hero_slides = list(hero_slides)

    # kiểm tra thêm lần nữa
    if not isinstance(hero_slides, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(hero_slides)}")
        return []

    # kiểm tra trong list này có dữ liệu hay không
    if not hero_slides:
        logger.warning("No hero slides found")
        return []

    # tạo list chunks
    chunks = []

    for idx, slide in enumerate(hero_slides):
        # kiểm tra từng slides có phải dict hay không
        if not isinstance(slide, dict):
            logger.warning(f"Invalid hero slides at index {idx}: {slide}")
            continue

        # mình quan tâm đến title, subtitle, description, imageUrl
        # lấy ra compnay title
        company_title = slide.get("title", "")
        if not company_title or not isinstance(company_title, str):
            logger.warning(f"Invalid company title at index {idx}: {company_title}")
            continue

        compnay_subtitle = slide.get("subtitle", "")
        if not compnay_subtitle or not isinstance(compnay_subtitle, str):
            logger.warning(f"Invalid company subtitle at index {idx}: {compnay_subtitle}")
            continue

        company_description = slide.get("description", "")
        if not company_description or not isinstance(company_description, str):
            logger.warning(f"Invalid company description at index {idx}: {company_description}")
            continue

        company_image_url = slide.get("imageUrl", "")
        if not isinstance(company_image_url, str):
            logger.warning(f"Invalid company image url at index {idx}: {company_image_url}")
            continue

        text_parts = [
            f"Lời mở đầu cho mục: {company_title} của công ty",
            f"Phụ đề mục {company_title}: {compnay_subtitle}",
            f"Mô tả chi tiết mục {company_title}: {company_description}",
        ]

        text = "\n".join(text_parts)
        # sau khi tạo ra được text thì mình cần thêm metadata vào
        chunks.append({
            "text": text,
            "metadata": {
                "type": "hero_slides",
                "source": "heroSlides.json",
                "slide_index": idx,
                "title": company_title,
                "subtitle": compnay_subtitle,
                "description": company_description,
                "image_url": company_image_url
            }
        })

    if not chunks:
        logger.warning("No chunks generated")
        return []

    logger.info(f"Successfully generated {len(chunks)} chunks from hero slides")

    return chunks
