from fastapi import FastAPI

from app.routers.webapp import router as webapp_router

app = FastAPI(title="Telegram Mini App Backend")
app.include_router(webapp_router)


@app.get("/", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
