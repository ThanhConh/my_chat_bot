from pathlib import Path
import json
import logging
from bs4 import BeautifulSoup
from core.setting_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def html_to_text(html:str) -> str:
    # lấy toàn bộ text trong HTML
    # seperator = " " chèn dấu khoảng cách giữa các đoạn text để tránh dính chữ
    # strip = True loại bỏ khoảng trắng ở đầu và cuối chuỗi
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def chunk_news():
    file_path = Path(settings["data"]["processed_dir"] / "news.json")

    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
            logger.info(f"Loaded {len(news_data)} news articles from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    if isinstance(news_data, dict):
        news_data = [news_data]

    if not isinstance(news_data, list):
        logger.error("Invalid news data format")
        return []
    
    if not news_data:
        logger.warning("No news found in the data") 
        return []

    chunks = []

    for idx, news_item in enumerate(news_data):
        if not isinstance(news_item, dict):
            logger.warning(f"Skipping invalid news item at index {idx}")
            continue

        news_title = news_item.get('title', '')
        if not news_title or not isinstance(news_title, str) or len(news_title.strip()) == 0:
            logger.warning(f"Skipping news item at index {idx} due to missing or invalid title")
            continue

        news_excerpt = news_item.get('excerpt', '')
        if not news_excerpt or not isinstance(news_excerpt, str):
            logger.warning(f"News item at index {idx} has no or invalid excerpt")
            continue

        news_content = news_item.get('content', '')
        if not news_content or not isinstance(news_content, str):
            logger.warning(f"News item at index {idx} has no or invalid content")
            continue

        news_content_text = html_to_text(news_content)
        news_image = news_item.get("thumbnailUrl")
        new_category = news_item.get("category")    
        new_category_id = new_item.get("categoryId")
        new_category_name = new_item.get("categoryName")
        new_category_slug = new_item.get("categorySlug")

        text_parts = [
            f"Tiêu đề tin tức: {news_title}",
            f"Tóm tắt tin tức: {news_excerpt}",
            f"Nội dung chi tiết tin tức: {news_content_text}",
        ]

        text = "\n".join(text_parts)

        chunk = {
            "text": text,
            "metadata": {
                "type": "news",
                "source": "news.json",
                "title": news_title,
                "excerpt": news_excerpt,
                "content": news_content_text,
                "image": news_image,
                "category": new_category,
                "category_id": new_category_id,
                "category_name": new_category_name,
                "category_slug": new_category_slug
            }
        }
        chunks.append(chunk)

    # Lưu 
    if not chunks:
        logger.warning("No chunks created")
        return []

    logger.info(f"Created {len(chunks)} chunks")
    return chunks

        