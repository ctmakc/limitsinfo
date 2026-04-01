import httpx
from typing import Dict, Any
from .base import BaseClient
from config import settings

class OpenAIClient(BaseClient):
    def __init__(self):
        super().__init__("openai")
        
    async def get_usage(self) -> Dict[str, Any]:
        """
        Fetch usage for OpenAI/Codex subscription.
        Currently returns mock data. Need to insert actual headers/cookies.
        """
        # TODO: Add real implementation reading from billing or Web API
        # Using settings.OPENAI_API_KEY or session cookie
        return {
            "current": 100000,
            "max": 500000,
            "next_reset": "2024-04-02 00:00:00"
        }

class ClaudeClient(BaseClient):
    def __init__(self):
        super().__init__("claude")
        
    async def get_usage(self) -> Dict[str, Any]:
        # Mock for Claude Pro limits
        return {
            "current": 15,
            "max": 45,
            "next_reset": "dynamic (2 hours)"
        }

class GeminiClient(BaseClient):
    def __init__(self):
        super().__init__("gemini")
        
    async def get_usage(self) -> Dict[str, Any]:
        # Mock for Gemini limits
        return {
            "current": 20,
            "max": 100,
            "next_reset": "daily"
        }

class PerplexityClient(BaseClient):
    def __init__(self):
        super().__init__("perplexity")
        
    async def get_usage(self) -> Dict[str, Any]:
        # Mock for Perplexity Pro
        return {
            "current": 250,
            "max": 600,
            "next_reset": "24 hours"
        }
