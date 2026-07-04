import logging

from core.settings_loader import load_settings
from embedding.embed_texts import embed_texts

settings = load_settings()
logger = logging.getLogger("batch_embed_texts")

EMBEDDING_BATCH_SIZE = settings["embedding"].get("batch_size", 32)

def batch_embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        logger.warning("No texts to embed")
        return []

    all_embeddings = []

    for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[start : start + EMBEDDING_BATCH_SIZE]

        batch_embeddings = embed_texts(batch)
        all_embeddings.extend(batch_embeddings)
        logger.info(f"Đã embed {len(all_embeddings)} / {len(texts)} texts")

    logger.info(f"Đã xử lý xong lô {len(all_embeddings)} vectors")

    return all_embeddings

