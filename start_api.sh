#!/bin/bash

# Hiển thị màu sắc cho đẹp
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}>>> Đang bật các container Docker (Qdrant & Ollama)...${NC}"
docker start qdrant ollama

echo -e "${BLUE}>>> Đang kích hoạt môi trường ảo (.venv) và khởi động API...${NC}"
source .venv/bin/activate
uvicorn api.app:app --reload --port 8000
