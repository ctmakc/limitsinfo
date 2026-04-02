import httpx
from typing import Dict, Any
import datetime
from .base import BaseClient
from settings_manager import secure_settings

class OpenAIClient(BaseClient):
    def __init__(self):
        super().__init__("openai")
        
    async def get_usage(self) -> Dict[str, Any]:
        """
        Fetch usage for OpenAI developer API.
        Attempts to access the billing dashboard endpoint.
        """
        api_key = secure_settings.get("OPENAI_API_KEY")
        if not api_key:
            return {"current": 0, "max": 0, "next_reset": "Unknown (API Key missing)"}
            
        now = datetime.datetime.now()
        start = now.replace(day=1).strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")
        
        async with httpx.AsyncClient() as client:
            try:
                # This is the historical endpoint for usage. Some accounts might restrict it.
                resp = await client.get(
                    f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start}&end_date={end}",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    # Data is usually in cents
                    used = data.get("total_usage", 0) / 100.0
                    hard_limit = 50.0  # Optional: hardcode or find in preferences endpoint
                    return {"current": used, "max": hard_limit, "next_reset": "Monthly"}
                else:
                    return {"current": 10, "max": 100, "next_reset": "API Error: " + str(resp.status_code)}
            except Exception as e:
                return {"current": 0, "max": 1, "next_reset": str(e)}

class ClaudeClient(BaseClient):
    def __init__(self):
        super().__init__("claude")
        
    async def get_usage(self) -> Dict[str, Any]:
        session_key = secure_settings.get("CLAUDE_SESSION_KEY")
        if not session_key:
            return {"current": 0, "max": 0, "next_reset": "Missing Key"}
        # Anthropic doesn't expose an API billing endpoint publicly yet.
        # Fallback to mock / hardcoded limits.
        return {
            "current": 15,
            "max": 45,
            "next_reset": "No Public Endpoint"
        }

class GeminiClient(BaseClient):
    def __init__(self):
        super().__init__("gemini")
        
    async def get_usage(self) -> Dict[str, Any]:
        return {
            "current": 20,
            "max": 100,
            "next_reset": "Google Cloud Quota"
        }

class PerplexityClient(BaseClient):
    def __init__(self):
        super().__init__("perplexity")
        
    async def get_usage(self) -> Dict[str, Any]:
        return {
            "current": 250,
            "max": 600,
            "next_reset": "24 hours"
        }
