import time
import uuid
import logging
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

from .config import settings
from .agent import run_travel_agent
from .redis_store import save_history, load_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

# ── Models ──
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

# ── Security Middleware ──
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != settings.AGENT_API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# ── Endpoints ──

@app.get("/")
def index():
    return {
        "message": "Welcome to TravelBuddy AI Agent!",
        "status": "Online",
        "documentation": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENVIRONMENT}

@app.post("/chat")
async def chat(body: ChatRequest, api_key: str = Depends(verify_api_key)):
    session_id = body.session_id or f"sess-{uuid.uuid4().hex[:8]}"
    
    # 1. Load history
    history = load_history(session_id)
    
    # 2. Run Agent
    start_time = time.time()
    try:
        response_text = await run_travel_agent(body.message, history)
    except Exception as e:
        logger.error(f"Agent Error: {e}")
        raise HTTPException(status_code=500, detail="Lỗi xử lý AI Agent")
    
    latency = round(time.time() - start_time, 2)
    
    # 3. Update History
    history.append({"role": "user", "content": body.message})
    history.append({"role": "assistant", "content": response_text})
    save_history(session_id, history)
    
    return {
        "session_id": session_id,
        "response": response_text,
        "latency_sec": latency,
        "served_by": "FastAPI-Production"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Starting TravelBuddy on port {settings.PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
