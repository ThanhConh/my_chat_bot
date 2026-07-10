import logging
import warnings

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv() # Load variables from .env before anything else is imported!

# Suppress the harmless joblib/loky semaphore leak warning on shutdown
warnings.filterwarnings("ignore", category=UserWarning, module="multiprocessing.resource_tracker")

from api.health import router as health_router  # noqa: E402
from api.routes.chat import chat  # noqa: E402

app = FastAPI(title="LTC Architecture Chatbot API")

# Setup CORS to allow Next.js frontend (port 3000) to communicate with FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[dict] | None = []

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Call the existing chat logic
        answer = chat(request.query)

        return ChatResponse(
            answer=answer,
            session_id=request.session_id or "new_session",
            sources=[]
        )
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
