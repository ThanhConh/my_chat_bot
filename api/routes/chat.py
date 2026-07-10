import logging

from core.schema import RetrieverDocument
from llm.generator import generate_answer
from retrieval.retriever import retrieve

logger = logging.getLogger("chat")

def chat(question: str) -> str:
    if not question or not question.strip():
        logging.warning("Empty question received")
        return "Please provide a non-empty question."

    logger.info(f"Received question: {question}")

    # Retrieve relevant document
    docs: list[RetrieverDocument] = retrieve(question)

    if not docs:
        logger.warning("No documents retrieved")
        context = ""
        return "I couldn't find relevant information for your question."
    else:
    # Format context
        context = "\n\n".join(f"[{i+1}] {doc.text}\n(Nguồn: {doc.metadata})" for i, doc in enumerate(docs))
        logger.info(f"Retrieved {len(docs)} documents")
        logger.info(f"Context: {context}")

        # Generate answer
        answer = generate_answer(context, question)
        logger.info(f"Generated answer: {answer}")

    return answer

