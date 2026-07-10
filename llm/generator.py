import logging

import ollama

from core.settings_loader import load_settings
from llm.prompt import build_prompt

settings = load_settings()
logger = logging.getLogger("llm")

LLM_CONFIG = settings["llm"]
MODEL_PROVIDER = LLM_CONFIG.get("provider")
MODEL_NAME = LLM_CONFIG.get("model_name","gpt-3.5-turbo")
MODEL_BASE_URL = LLM_CONFIG.get("base_url","http://localhost:11434")
MODEL_TEMPERATURE = LLM_CONFIG.get("temperature",0.2)
MODEL_MAX_TOKENS = LLM_CONFIG.get("max_tokens",512)
MODEL_TIMEOUT = LLM_CONFIG.get("timeout",60)

def generate_answer(context:str, question:str):
    if not context or not context.strip():
        logger.error("Context or question is empty")
        return "Không thể tạo câu trả lời do thiếu thông tin."
    if not question or not question.strip():
        logger.error("Context or question is empty")
        return "Không thể tạo câu trả lời do thiếu thông tin."

    prompt = build_prompt(context,question)

    try:
        if MODEL_PROVIDER == "ollama":
            client = ollama.Client(host=MODEL_BASE_URL,timeout=MODEL_TIMEOUT)
            response = client.chat(
                model = MODEL_NAME,
                messages = [
                    {"role": "system", "content": prompt}
                ],
                options={
                    "temperature": MODEL_TEMPERATURE,
                    "num_predict": MODEL_MAX_TOKENS,
                }
            )
            answer = response['message']['content'].strip()
        else:
            logger.error("Unsupported model provider")
            return "Không thể tạo câu trả lời do lỗi hệ thống."
        return answer
    except ollama.ResponseError as e:
        logger.error(f"Error generating answer: {e}")
        return "Không thể tạo câu trả lời do lỗi hệ thống."
    except ollama.RequestError as e:
        logger.error(f"Error generating answer: {e}")
        return "Không thể tạo câu trả lời do lỗi hệ thống."
    except TimeoutError:
        logger.error("Error generating answer: Timeout")
        return "Không thể tạo câu trả lời do timeout."
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Không thể tạo câu trả lời do lỗi hệ thống."

