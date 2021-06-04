from aiomono.exceptions import MonoException


def validate_token(token: str):
    if not isinstance(token, str):
        raise MonoException(f"Token is invalid! It must be 'str' type instead of {type(token)} type.")
