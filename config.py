import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    
    # Check Interval (in minutes)
    CHECK_INTERVAL_MINUTES: int = 15
    
    # API Keys for Developer APIs
    OPENAI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    
    # Platform Cookies / Tokens (for Web reversing if needed)
    CURSOR_TOKEN: str = ""
    CLAUDE_SESSION_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
