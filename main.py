import asyncio

from fastapi import FastAPI

from app.bot import build_bot, build_dispatcher
from app.config import get_settings

settings = get_settings()
bot = build_bot(settings)
dispatcher = build_dispatcher()

app = FastAPI(title="Telegram Mini App Bot")


@app.on_event("startup")
async def on_startup() -> None:
    app.state.polling_task = asyncio.create_task(dispatcher.start_polling(bot))


@app.on_event("shutdown")
async def on_shutdown() -> None:
    polling_task: asyncio.Task = app.state.polling_task
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()


@app.get("/", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/webapp", tags=["webapp"])
async def webapp_entry() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Telegram Mini App работает",
    }
