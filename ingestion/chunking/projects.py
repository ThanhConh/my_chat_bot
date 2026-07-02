import logging
import json
from pathlib import Path

from core.settings_loader import load_settings

logger = logging.getLogger("ingestion")

settings = load_settings()

def chunk_projects():
    file_path = Path(settings["data"]["processed_dir"] / "projects.json")

    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            projects = json.load(file)
            logger.info(f"Loaded {len(projects)} projects from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    if isinstance(projects, dict):
        projects = list(projects.values())

    if not isinstance(projects, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(projects)}")
        return []

    if not projects:
        logger.warning(f"No projects found in {file_path}")
        return []

    chunks = []
    for idx, project in enumerate(projects):
        if not isinstance(project, dict):
            logger.warning(f"Invalid project data at index {idx}: {project}")
            continue

        project_id = project.get("id")
        project_title = project.get("title", "")
        if not project_title or not isinstance(project_title, str):
            logger.warning(f"Skipping project with invalid title at index {   idx}")
            continue

        project_slug = project.get("slug", "")
        
        project_description = project.get("description", "")
        
        project_investor = project.get("investor", "")
        project_location = project.get("location")
        project_area = project.get("area", "")
        project_complet_data = project.get("completedDate", "")
        project_vew_count = project.get("view_count", "")

        project_category = project.get("category", {}) # tại vì category là 1 list chứa nhiều dict
        if not isinstance(project_category, dict):
            project_category = {}
            logger.warning(f"Invalid project category data at index {idx}: {project_category}")
            
        project_category_id = project_category.get("id")
        project_category_name = project_category.get("name", "")
        if not project_category_name or not isinstance(project_category_name, str):
            logger.warning(f"Invalid project category name at index {idx}: {project_category_name}")
            continue
        project_category_slug = project_category.get("slug")


        project_interior_style = project.get("interiorStyle", {})
        if not project_interior_style or not isinstance(project_interior_style, dict):
            project_interior_style = {}
            logger.warning(f"Invalid project interior style data at index {idx}: {project_interior_style}")
        project_interior_style_id = project_interior_style.get("id")
        project_interior_style_name = project_interior_style.get("name", "")
        if not project_interior_style_name or not isinstance(project_interior_style_name, str):
            logger.warning(f"Invalid project interior style name at index {idx}: {project_interior_style_name}")
            continue
        project_interior_style_slug = project_interior_style.get("slug")

        project_architecture_type = project.get("architectureType", {})
        if not project_architecture_type or not isinstance(project_architecture_type, dict):
            project_architecture_type = {}
            logger.warning(f"Invalid project architecture type data at index {idx}: {project_architecture_type}")

        project_architecture_type_id = project_architecture_type_data.get("id")

        project_architecture_type_name = project_architecture_type_data.get("name", "")
        if not project_architecture_type_name or not isinstance(project_architecture_type_name, str):
            logger.warning(f"Invalid project architecture type name at index {idx}: {project_architecture_type_name}")
            continue
        
        project_architecture_type_slug = project_architecture_type_data.get("slug")

        text_parts = [
            f"Tên dự án: {project_title}",
            f"Slug dự án: {project_slug}",
            f"Mô tả dự án: {project_description}",
            f"Nhà đầu tư dự án: {project_investor}",
            f"Địa chỉ dự án: {project_location}",
            f"Diện tích dự án: {project_area}",
            f"Ngày hoàn thành dự án: {project_complet_data}",
            f"Lượt xem dự án: {project_vew_count}",
            f"Danh mục dự án: {project_category_name}",
            f"Phong cách thiết kế: {project_interior_style_name}",
            f"Loại kiến trúc: {project_architecture_type_name}",
        ]

        text = "\n".join(text_parts)

        chunks.append({
            "text": text,
            "metadata": {
                "type": "project",
                "source": "projects.json",
                "project_id": project_id,
                "project_title": project_title,
                "project_slug": project_slug,
                "project_description": project_description,
                "project_investor": project_investor,
                "project_location": project_location,
                "project_area": project_area,
                "project_complet_data": project_complet_data,
                "project_vew_count": project_vew_count,
                "project_category_id": project_category_id,
                "project_category_name": project_category_name,
                "project_category_slug": project_category_slug,
                "project_interior_style_id": project_interior_style_id,
                "project_interior_style_slug": project_interior_style_slug,
                "project_interior_style_name": project_interior_style_name,
                "project_architecture_type_id": project_architecture_type_id,
                "project_architecture_type_slug": project_architecture_type_slug,
                "project_architecture_type_name": project_architecture_type_name,
            },
        })

    if not chunks:
        logger.warning("No chunks generated")
        return []
    logger.info(f"Successfully generated {len(chunks)} chunks from projects")
    return chunks