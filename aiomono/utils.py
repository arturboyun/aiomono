from aiomono.exceptions import MonoException


def validate_token(token: str) -> bool:
    if not isinstance(token, str):
        raise MonoException(f"Token is invalid! It must be 'str' type instead of {type(token)} type.")
    return True
