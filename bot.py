import httpx


class TelegramBotApiError(RuntimeError):
    """Raised when Telegram Bot API request fails."""


class TelegramBotService:
    def __init__(self, bot_token: str, mini_app_url: str) -> None:
        self.bot_token = bot_token
        self.mini_app_url = mini_app_url

    @property
    def base_url(self) -> str:
        return f"https://api.telegram.org/bot{self.bot_token}"

    def build_first_message_payload(
        self,
        chat_id: int | str,
        text: str,
        button_text: str,
    ) -> dict:
        return {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": button_text,
                            "web_app": {
                                "url": self.mini_app_url,
                            },
                        }
                    ]
                ]
            },
        }

    async def send_first_message(
        self,
        chat_id: int | str,
        text: str,
        button_text: str,
    ) -> dict:
        payload = self.build_first_message_payload(chat_id, text, button_text)

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(f"{self.base_url}/sendMessage", json=payload)

        if response.status_code != 200:
            raise TelegramBotApiError(
                f"Telegram Bot API returned status {response.status_code}"
            )

        data = response.json()
        if not data.get("ok"):
            raise TelegramBotApiError(
                f"Telegram Bot API error: {data.get('description', 'unknown error')}"
            )

        return data
