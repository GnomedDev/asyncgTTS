from aiohttp import ClientSession

from .asyncgTTS import asyncgTTS
from .easygTTS import easygTTS
from .errors import *

__all__ = ("setup", )

async def setup(premium: bool, *args, **kwargs):
    if not kwargs.get("session"):
        kwargs["session"] = ClientSession()

    gtts = asyncgTTS if premium else easygTTS
    return gtts(*args, **kwargs)
