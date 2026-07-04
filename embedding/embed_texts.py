import logging

import numpy as np
from transformers import SentenceTransformer

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("embedding")

EMBEDDING_MODEL = settings["embedding"]["model"]
EMBEDDING_DEVICE = settings["embedding"].get("device", "cpu")
EMBEDDING_BATCH_SIZE = settings["embedding"]["batch_size"]

# khởi tạo model là 1 biến global
_model = None

# design pattern singleton để khởi tạo model
def get_model():
    global _model
    if _model is None:
        logger.info(f"Loading SentenceTransformer model from {EMBEDDING_MODEL} with device {EMBEDDING_DEVICE}")
        _model = SentenceTransformer(EMBEDDING_MODEL, device=EMBEDDING_DEVICE)
        logger.info("Model loaded successfully")
    return _model

# hàm embedding: input chuỗi string => chuỗi chứa các float
def embed_texts(texts: list[str]) -> np.ndarray:
    if not texts:
        logger.warning("No texts to embed")
        return np.array([])

    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True, convert_to_tensor=False).tolist()
    logger.info(f"Completed embedding {len(texts)} texts")
    return embeddings
