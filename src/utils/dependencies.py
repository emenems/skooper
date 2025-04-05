import os
import binascii
from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEYS = os.getenv("API_KEY", default=binascii.hexlify(os.urandom(32)).decode()).split(",")


async def api_key_auth(x_api_key: Annotated[str, Header()]):
    """API key authentication"""
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=400, detail="X-Api-Key header invalid")
    return x_api_key
