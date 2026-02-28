import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from app.models.user import TelegramUser


class TelegramInitDataError(ValueError):
    """Raised when Telegram init data is invalid."""


class TelegramService:
    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token

    def validate_init_data(self, init_data: str) -> dict[str, str]:
        if not init_data:
            raise TelegramInitDataError("initData is missing")

        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = pairs.pop("hash", None)
        if not received_hash:
            raise TelegramInitDataError("hash is missing in initData")

        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(pairs.items())
        )
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=self.bot_token.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            raise TelegramInitDataError("invalid initData signature")

        return pairs

    def parse_user(self, validated_init_data: dict[str, str]) -> TelegramUser:
        user_raw = validated_init_data.get("user")
        if not user_raw:
            raise TelegramInitDataError("user is missing in initData")

        try:
            user_payload = json.loads(user_raw)
        except json.JSONDecodeError as exc:
            raise TelegramInitDataError("user payload is not valid JSON") from exc

        return TelegramUser.model_validate(user_payload)
