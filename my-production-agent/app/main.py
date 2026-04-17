import json
import logging
from contextlib import asynccontextmanager

import redis
import httpx
from fastapi import Depends, FastAPI, HTTPException, Header, JSONResponse
from pydantic import BaseModel

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)
logger = logging.getLogger(__name__)

r = redis.from_url(settings.REDIS_URL)


class AskRequest(BaseModel):
    question: str
    user_id: str


class TokenRequest(BaseModel):
    username: str
    password: str


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting agent...")
    yield
    logger.info("Shutting down agent...")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    """Liveness probe - container còn sống không?"""
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Readiness probe - sẵn sàng nhận traffic không?"""
    try:
        r.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "not ready"}
        )


@app.post("/token")
def get_token(request: TokenRequest):
    """Get JWT token (mock implementation)"""
    if request.username == "admin" and request.password == "secret":
        # In production, use python-jose to create real JWT
        return {"access_token": "mock-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/ask")
def ask(
    request: AskRequest,
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(lambda: check_rate_limit(request.user_id)),
    _budget: None = Depends(lambda: check_budget(request.user_id))
):
    """
    Main endpoint: Ask question to AI agent.
    - Verify API key
    - Check rate limit
    - Check budget
    - Get conversation history from Redis
    - Call LLM
    - Save to Redis
    - Return response
    """
    if user_id != request.user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # 1. Get conversation history từ Redis
    history_key = f"history:{request.user_id}"
    history = json.loads(r.get(history_key) or "[]")

    # 2. Build messages và gọi LLM
    messages = history + [{"role": "user", "content": request.question}]
    response = call_llm(messages)

    # 3. Save to Redis
    history.append({"role": "user", "content": request.question})
    history.append({"role": "assistant", "content": response})
    r.setex(history_key, 7 * 24 * 3600, json.dumps(history))

    logger.info(f"User {request.user_id} asked: {request.question[:50]}...")

    return {"answer": response, "user_id": request.user_id}


def call_llm(messages: list) -> str:
    """
    Mock LLM - trả về canned responses.
    Thay bằng OpenAI/Claude thật khi cần.
    """
    last_msg = messages[-1]["content"].lower()

    if "hello" in last_msg or "hi" in last_msg:
        return "Hello! How can I help you today?"
    elif "docker" in last_msg:
        return "Docker is a containerization platform that packages your application with its dependencies into a container."
    elif "kubernetes" in last_msg or "k8s" in last_msg:
        return "Kubernetes is a container orchestration platform for automating deployment, scaling, and management."
    elif "api" in last_msg:
        return "An API (Application Programming Interface) allows different software applications to communicate with each other."
    elif "database" in last_msg or "db" in last_msg:
        return "A database is an organized collection of structured information stored electronically in a computer system."
    elif "cache" in last_msg or "redis" in last_msg:
        return "Redis is an in-memory data structure store used as a database, cache, and message broker."

    return f"You asked: '{messages[-1]['content']}'. This is a mock AI response. In production, this would call OpenAI or Claude."


@app.post("/shutdown")
def shutdown():
    """Graceful shutdown endpoint (for testing)"""
    logger.info("Shutdown signal received")
    return {"message": "Shutting down..."}
