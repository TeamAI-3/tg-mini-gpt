# backend/telegram_auth.py
from future import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import parse_qsl


@dataclass
class TelegramInitData:
    raw: str
    data: Dict[str, Any]
    user: Optional[Dict[str, Any]]


def _constant_time_equal(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def validate_init_data(init_data: str, bot_token: str) -> TelegramInitData:
    """
    Validates Telegram WebApp initData.

    init_data: querystring from tg.initData
    bot_token: token from BotFather

    Returns parsed data and user dict (if present).
    Raises ValueError if invalid.
    """
    init_data = (init_data or "").strip()
    if not init_data:
        # allow empty for browser testing
        return TelegramInitData(raw="", data={}, user=None)

    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.get("hash")
    if not received_hash:
        raise ValueError("initData has no hash")

    # remove hash for check string
    pairs.pop("hash", None)

    # build data_check_string: key=value \n sorted by key
    items = sorted((k, v) for k, v in pairs.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in items])

    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not _constant_time_equal(calculated_hash, received_hash):
        raise ValueError("initData hash is invalid")

    # parse user if present
    user_obj = None
    if "user" in pairs:
        try:
            user_obj = json.loads(pairs["user"])
        except Exception:
            user_obj = None

    # return everything (including received hash? not needed usually)
    parsed: Dict[str, Any] = dict(pairs)
    parsed["hash"] = received_hash
    return TelegramInitData(raw=init_data, data=parsed, user=user_obj)