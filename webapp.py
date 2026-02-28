from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.config import Settings, get_settings
from app.services.telegram import TelegramInitDataError, TelegramService

router = APIRouter(prefix="/webapp", tags=["webapp"])


def get_telegram_service(settings: Settings = Depends(get_settings)) -> TelegramService:
    return TelegramService(bot_token=settings.bot_token)


@router.get("")
async def webapp_entry(
    init_data_query: str | None = Query(default=None, alias="initData"),
    init_data_header: str | None = Header(default=None, alias="X-Telegram-Init-Data"),
    telegram_service: TelegramService = Depends(get_telegram_service),
) -> dict:
    init_data = init_data_header or init_data_query
    if not init_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram initData is required in X-Telegram-Init-Data header or initData query parameter",
        )

    try:
        validated_data = telegram_service.validate_init_data(init_data)
        user = telegram_service.parse_user(validated_data)
    except TelegramInitDataError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return {
        "ok": True,
        "user": user.model_dump(),
    }
