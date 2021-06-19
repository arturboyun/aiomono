import os
import ecdsa
import base64
import hashlib
import binascii

from aiomono import MonoException


def load_sign_key(private_key: str) -> ecdsa.SigningKey:
    if "PRIVATE KEY-----" in private_key:
        raw = private_key
    elif os.path.exists(private_key):
        with open(private_key) as f:
            raw = f.read()
    else:
        raise MonoException("Cannot load private key")
    return ecdsa.SigningKey.from_pem(raw)


class SignKey(object):
    def __init__(self, private_key: str):
        self.private_key = private_key
        self.sign_key = load_sign_key(self.private_key)

    def key_id(self) -> bytes:
        """Returns monobank X-Key-Id"""
        public_key = self.sign_key.get_verifying_key()
        uncompressed_public_key = bytearray([0x04]) + (bytearray(public_key.to_string()))
        digests = hashlib.sha1()
        digests.update(uncompressed_public_key)
        return binascii.hexlify(digests.digest())

    def sign(self, str_to_sign: str) -> bytes:
        """Signs string str_to_sign with private key, and hash sha256"""
        sign = self.sign_key.sign(str_to_sign.encode(), hashfunc=hashlib.sha256)
        return base64.b64encode(sign)
