# trong retrieval/retriever.py nhận được 1 question - query - embedding vector thành - so sánh vector querry với các vector trong các chunk
import logging

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.models import ScoredPoint

from core.schema import RetrieverDocument
from core.settings_loader import load_settings
from embedding.embed_texts import embed_texts
from vectorstore.qdrant import get_qdrant_client

settings = load_settings()
logger = logging.getLogger("retrieval")

RETRIEVAL_CONFIG = settings.get("retrieval")
COLLECTION_NAME = settings["vector_database"]["collection_name"]
TOP_K = RETRIEVAL_CONFIG.get("top_k", 5)
RETRIEVAL_SCORE_THRESHOLD = RETRIEVAL_CONFIG.get("score_threshold", 0.3)

def retrieve(query: str) -> list[RetrieverDocument]:
    if not query:
        logger.warning("Empty query received for retrieval.")
        return []
    try:
        client: QdrantClient = get_qdrant_client()
        vectors = embed_texts([query])
        if not vectors:
            logger.error("No vectors generated")
            return []

        query_vector = vectors[0]
        response = client.query_points(collection_name=COLLECTION_NAME,
         query=query_vector,
         limit=TOP_K,
         with_payload=True,
         score_threshold=RETRIEVAL_SCORE_THRESHOLD)

        # response chứa các point và trong các point này là các ScoredPoint
        points: list[ScoredPoint] = response.points if hasattr(response, 'points') else response # : là để chú thích
        documents: list[RetrieverDocument] = []
        for point in points:
            payload = point.payload or {} # nếu không có payload trả về 1 dict rỗng

            documents.append(
                RetrieverDocument(
                    id=str(point.id),
                    score=point.score,
                    text=payload.get("text", ""),
                    metadata={
                        key:value for key, value in payload.items() if key != "text"
                    }
                )
            )
        logger.info(f"Retrieved {len(documents)} documents")
        return documents

    except ResponseHandlingException as e:
        logger.error(f"Error in retrieval: {e}")
        raise ConnectionError("Database connection failed") from e
    except Exception as e:
        logger.error(f"Unexpected error in retrieval: {e}")
        return []
