from contextlib import asynccontextmanager
import asyncio
import traceback

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Body, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from clients.models import ClaudeClient, GeminiClient, OpenAIClient, PerplexityClient
from config import settings
from settings_manager import secure_settings
from state_manager import state
from telegram_bot import send_telegram_alert

scheduler = AsyncIOScheduler()

clients = [
    OpenAIClient(),
    ClaudeClient(),
    GeminiClient(),
    PerplexityClient(),
]


async def check_all_limits():
    print("Checking AI limits (cron job)...")
    for client in clients:
        try:
            usage = await client.get_usage()
            current = usage["current"]
            max_limit = usage["max"]
            next_reset = usage.get("next_reset", "Unknown")

            if max_limit <= 0:
                state.update_limit(client.name, 0, 0, next_reset)
                continue

            percent_used = (current / max_limit) * 100
            percent_remaining = 100 - percent_used

            print(
                f"[{client.name.upper()}] Used: {current}/{max_limit} "
                f"({percent_used:.1f}%) | Remaining: {percent_remaining:.1f}%"
            )

            old_state = state.get_limit(client.name)
            last_alert = old_state.get("last_alerted_level", 100)

            state.update_limit(client.name, current, max_limit, next_reset)

            if percent_remaining == 100 and last_alert < 100:
                await send_telegram_alert(
                    f"[RESET] <b>{client.name.upper()}</b> limits have been reset!\nRemaining: 100%"
                )
                state.set_alert_level(client.name, 100)
            elif percent_remaining <= 0 and last_alert > 0:
                await send_telegram_alert(
                    f"[CRITICAL] <b>{client.name.upper()}</b> OUT OF LIMITS!\nRemaining: 0%"
                )
                state.set_alert_level(client.name, 0)
            elif percent_remaining <= 25 and last_alert > 25:
                await send_telegram_alert(
                    f"[WARN] <b>{client.name.upper()}</b> limits are dropping low!\n"
                    f"Remaining: {percent_remaining:.1f}%"
                )
                state.set_alert_level(client.name, 25)
            elif percent_remaining <= 50 and last_alert > 50:
                await send_telegram_alert(
                    f"[INFO] <b>{client.name.upper()}</b> limits are at half capacity.\n"
                    f"Remaining: {percent_remaining:.1f}%"
                )
                state.set_alert_level(client.name, 50)

        except Exception as e:
            print(f"Error checking {client.name}: {e}")
            traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting...")
    asyncio.create_task(check_all_limits())
    scheduler.add_job(check_all_limits, "interval", minutes=settings.CHECK_INTERVAL_MINUTES)
    scheduler.start()

    asyncio.create_task(send_telegram_alert("[STARTED] <b>AI Limits Monitor</b> started!"))

    yield
    print("Application shutting down...")
    scheduler.shutdown()


app = FastAPI(title="AI Limits Monitor", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_dashboard():
    return FileResponse("static/index.html")


@app.get("/api/limits")
async def get_limits():
    return {
        "services": [
            {"service": "openai", "name": "OpenAI", **state.get_limit("openai")},
            {"service": "claude", "name": "Claude", **state.get_limit("claude")},
            {"service": "gemini", "name": "Gemini", **state.get_limit("gemini")},
            {"service": "perplexity", "name": "Perplexity", **state.get_limit("perplexity")},
        ]
    }


class SettingsModel(BaseModel):
    OPENAI_API_KEY: str | None = None
    CLAUDE_SESSION_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    PERPLEXITY_API_KEY: str | None = None


@app.get("/api/settings")
async def get_settings():
    return secure_settings.get_public_status()


@app.post("/api/settings")
async def update_settings(data: SettingsModel):
    if data.OPENAI_API_KEY is not None:
        secure_settings.set("OPENAI_API_KEY", data.OPENAI_API_KEY)
    if data.CLAUDE_SESSION_KEY is not None:
        secure_settings.set("CLAUDE_SESSION_KEY", data.CLAUDE_SESSION_KEY)
    if data.GEMINI_API_KEY is not None:
        secure_settings.set("GEMINI_API_KEY", data.GEMINI_API_KEY)
    if data.PERPLEXITY_API_KEY is not None:
        secure_settings.set("PERPLEXITY_API_KEY", data.PERPLEXITY_API_KEY)
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
