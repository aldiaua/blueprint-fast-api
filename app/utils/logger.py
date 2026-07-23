import json

SENSITIVE_FIELDS = {
    "password",
    "confirm_password",
    "old_password",
    "new_password",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "secret",
    "api_key",
}


def mask_data(data):
    if isinstance(data, dict):
        return {
            key: (
                "******"
                if key.lower() in SENSITIVE_FIELDS
                else mask_data(value)
            )
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [mask_data(item) for item in data]

    return data


def parse_request_body(body: bytes):
    """
    Parse request body menjadi object Python.
    """
    if not body:
        return None

    try:
        return mask_data(json.loads(body.decode()))
    except Exception:
        return body.decode(errors="ignore")