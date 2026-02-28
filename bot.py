from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from app.config import Settings

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    settings = message.bot["settings"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть мини-приложение",
                    web_app=WebAppInfo(url=settings.webapp_url),
                )
            ]
        ]
    )

    await message.answer(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=keyboard,
    )


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)
    return dp


def build_bot(settings: Settings) -> Bot:
    bot = Bot(token=settings.bot_token)
    bot["settings"] = settings
    return bot
