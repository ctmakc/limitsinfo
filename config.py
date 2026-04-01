import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    
    # Check Interval (in minutes)
    CHECK_INTERVAL_MINUTES: int = 15
    
    # Platform Cookies / Tokens
    CURSOR_TOKEN: str = ""
    CLAUDE_SESSION_KEY: str = ""
    GEMINI_SESSION: str = ""
    PERPLEXITY_SESSION: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
