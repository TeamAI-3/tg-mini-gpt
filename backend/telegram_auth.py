import hmac, hashlib
from urllib.parse import parse_qsl

def verify_telegram_init_data(init_data: str, bot_token: str) -> dict:
    data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop("hash", None)
    if not received_hash:
        raise ValueError("No hash in initData")

    pairs = [f"{k}={data[k]}" for k in sorted(data.keys())]
    data_check_string = "\n".join(pairs)

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()

    calc_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calc_hash, received_hash):
        raise ValueError("Bad initData signature")

    return data