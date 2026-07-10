# nhập 1 question và question sẽ được đưa qua thằng retriever để lấy những vecto rồi mình so sánh với vecto store trong gdrant
# build promp sinh ra câu trả lời là xong
import logging
import os

from core.settings_loader import load_settings
from llm.generator import generate_answer
from retrieval.retriever import retrieve

settings = load_settings()
logger = logging.getLogger("chat")

MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "512"))

def chat(question: str) -> str:
    if not question:
        logger.warning("Question is empty")
        return ""

    if len(question) > MAX_QUERY_LENGTH:
        logger.warning("Question is too long")
        return "Câu hỏi vượt quá độ dài cho phép"

    logger.info(f"Starting retrieval for the question {question}.")

    try:
        documents = retrieve(question)

        if not documents:
            logger.info("No relevant documents found")
            return "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn trong tài liệu."
        # [1] Nội dung context 1
        # {nguồn {}}
        context = "\n\n".join(
            f"[{i+1}] {doc.text}\n(Nguồn: {doc.metadata})"
            for i, doc in enumerate(documents)
        )
        answer = generate_answer(context,question)
        logger.info("Generated answer successfully")
        return answer

    #except xử lý lỗi
    except ValueError as e:
        logger.error(f"Value error during retrieval: {e}")
        return "Xin lỗi, đã xảy ra lỗi trong quá trình xử lý yêu cầu của bạn."

    except Exception as e:
        logger.error(f"Unexpected error during retrieval: {e}")
        return "Xin lỗi, đã xảy ra lỗi hệ thống."

def main():
    while True:
        question = input("Bạn: ")
        if question.lower() in {"exit", "quit"}:
            break
        answer = chat(question)
        print("Bot:", answer)
        logger.info(f"Answer: {answer}")

if __name__ == "__main__":
    main()
