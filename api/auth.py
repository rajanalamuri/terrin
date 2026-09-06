import hashlib
import hmac
import secrets

from api.db import get_device


def generate_api_key():
    return secrets.token_urlsafe(32)


def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_device(device_id, api_key):
    if not api_key:
        return False
    device = get_device(device_id)
    if not device:
        return False
    return hmac.compare_digest(device["api_key_hash"], hash_api_key(api_key))
