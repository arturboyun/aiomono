from datetime import datetime, timezone

from aiomono.exceptions import MonoException


def validate_token(token: str):
    """Validates Monobank API Token"""
    if not isinstance(token, str):
        raise MonoException(f"Token is invalid! It must be 'str' type instead of {type(token)} type.")


def to_timestamp(datetime_: datetime) -> int:
    """Converts datetime to timestamp"""
    return int(datetime_.replace(tzinfo=timezone.utc).timestamp())
