import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "TravelBuddy-Production"
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # API Security
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "travel-secret-123")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-travel")
    
    # AI Client (OpenRouter)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    MODEL_NAME: str = "qwen/qwen-2.5-72b-instruct"
    
    # Redis for Stateless History
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Budget Guard
    DAILY_BUDGET_USD: float = 2.0  # $2 per day limit for Travel AI

    class Config:
        env_file = ".env"

settings = Settings()
