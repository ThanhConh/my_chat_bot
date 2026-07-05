import json
import logging
from pathlib import Path

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_company_info():
    file_path = Path(settings["data"]["processed_dir"]) / "companyInfo.json"

    # kiểm tra đường dẫn tồn tại không
    if not file_path.exists():
        logger.error(f"File not found {file_path}")
        return []

    # lấy data từ companyInfo
    # đọc file đó lên
    try:
        with open(file_path, encoding="utf-8") as file:
            company_info = json.load(file) # file không phải file Path
            logger.info(f"Loaded {len(company_info)} records from {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {file_path}: {e}")
        return []

    # sau khi mở file => tiếp tục kiểm tra company phải list hay khong. bởi vì trong company info có thể chứa nhiều item con. Một item là 1 dict và phải là 1 list chứa nhiều dict
    if isinstance(company_info, dict):
        company_info = list(company_info) # convert sang list nếu nó là dict

    # kiểm tra thêm lần nữa
    if not isinstance(company_info, list):
        logger.error(f"Invalid data format in {file_path}. Expected a list, got {type(company_info)}")
        return []

    # kiểm tra xem có dữ liệu trong compnay hay không
    if not company_info:
        logger.warning("No company info found")
        return []

    # tạo list chunks
    chunks = []

    for idx, info in enumerate(company_info):
        if not isinstance(info, dict):
            logger.warning(f"Invalid item at index {idx}: {info}")
            continue

        company_name = info.get("companyName", "")
        # kiểm tra company name có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_name, str) or not company_name:
            logger.warning(f"Company name at index {idx} is invalid")
            continue

        company_slogan = info.get("companySlogan", "")
        # kiểm tra company slogan có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_slogan, str) or not company_slogan:
            logger.warning(f"Company slogan at index {idx} is invalid")
            continue

        company_description = info.get("companyDescription", "")
        # kiểm tra company description có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_description, str) or not company_description:
            logger.warning(f"Company description at index {idx} is invalid")
            continue

        compnay_hotlines = info.get("hotlines", [])
        # kiểm tra hotlines có dữ liệu và có phải list hay không
        if not isinstance(compnay_hotlines, list):
            logger.warning(f"Hotlines at index {idx} is invalid")
            continue

        company_emails = info.get("emails",[])
        # kiểm tra emails có dữ liệu và có phải list hay không
        if not isinstance(company_emails, list):
            logger.warning(f"Emails at index {idx} is invalid")
            continue

        company_main_address = info.get("mainAddress", "")
        # kiểm tra main address có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_main_address, str):
            logger.warning(f"Main address at index {idx} is invalid")
            continue
        company_working_hours = info.get("workingHours", "")
        # kiểm tra working hours có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_working_hours, str):
            logger.warning(f"Working hours at index {idx} is invalid")
            continue

        company_website = info.get("website", "")
        # kiểm tra website có dữ liệu và có phải chuỗi hay không
        if not isinstance(company_website, str) or not company_website:
            logger.warning(f"Website at index {idx} is invalid")
            continue

        company_social_links = info.get("socialLinks", {})
        # kiểm tra social links có dữ liệu và có phải dict hay không
        if not isinstance(company_social_links, dict) or not company_social_links:
            logger.warning(f"Social links at index {idx} is invalid")
            continue
        # xử lý các gía trị null của social links
        if isinstance(company_social_links, dict):
            company_social_text = ", ".join([f"{k}: {v}" for k, v in company_social_links.items() if v])


        company_total_employees = info.get("totalEmployees")
        # kiểm tra total employees có dữ liệu và có phải số hay không
        if not isinstance(company_total_employees, (int, float)) or not company_total_employees:
            logger.warning(f"Total employees at index {idx} is invalid")
            continue

        company_total_projects = info.get("totalProjects")
        # kiểm tra total projects có dữ liệu và có phải số hay không
        if not isinstance(company_total_projects, (int, float)) or not company_total_projects:
            logger.warning(f"Total projects at index {idx} is invalid")
            continue

        # ở đây với list thì mình cần dấu phẩy và dấu cách để nó tự tách các kí tự thành các chuỗi
        text_parts = [
            f"Tên công ty: {company_name}",
            f"Khẩu hiệu công ty: {company_name}: {company_slogan}",
            f"Mô tả công ty: {company_name}: {company_description}",
            f"Số điện thoại công ty: {company_name}: {', '.join(compnay_hotlines)}",
            f"Email công ty: {company_name}: {', '.join(company_emails)}",
            f"Địa chỉ chính công ty: {company_name}: {company_main_address}",
            f"Giờ làm việc công ty: {company_name}: {company_working_hours}",
            f"Website công ty: {company_name}: {company_website}",
            f"Social links công ty: {company_name}: {company_social_text}",
            f"Tổng số nhân viên công ty: {company_name}: {company_total_employees}",
            f"Tổng số dự án công ty: {company_name}: {company_total_projects}",
        ]

        text = "\n".join(text_parts)

        chunk = {
            "text": text,
            "metadata": {
                "type": "companyInfo",
                "source": "companyInfo.json", # nguồn lấy thông tin chính là file json
                "company_name": company_name,
                "company_slogan": company_slogan,
                "company_description": company_description,
                "company_hotlines": compnay_hotlines,
                "company_emails": company_emails,
                "company_main_address": company_main_address,
                "company_working_hours": company_working_hours,
                "company_website": company_website,
                "company_social_links": company_social_links,
                "company_total_employees": company_total_employees,
                "company_total_projects": company_total_projects,
            }
        }
        chunks.append(chunk)

    if not chunks:
        logger.warning("No chunks generated")
        return []

    logger.info(f"Successfully generated {len(chunks)} chunks from company info")
    return chunks
