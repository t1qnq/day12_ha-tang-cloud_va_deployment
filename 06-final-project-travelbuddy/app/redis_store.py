import json
import logging
from .config import settings

try:
    import redis
    _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    _redis.ping()
    USE_REDIS = True
    logging.info("✅ Connected to Redis for Stateless Sessions")
except Exception as e:
    logging.warning(f"⚠️ Redis not available: {e}. Falling back to in-memory (not scalable!)")
    USE_REDIS = False
    _memory_store = {}

def save_history(session_id: str, history: list, ttl: int = 3600):
    """Lưu lịch sử chat vào Redis."""
    if USE_REDIS:
        _redis.setex(f"travel_chat:{session_id}", ttl, json.dumps(history))
    else:
        _memory_store[session_id] = history

def load_history(session_id: str) -> list:
    """Tải lịch sử chat từ Redis."""
    if USE_REDIS:
        data = _redis.get(f"travel_chat:{session_id}")
        return json.loads(data) if data else []
    return _memory_store.get(session_id, [])
