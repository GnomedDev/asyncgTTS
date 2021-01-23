from aiohttp import ClientSession

from .asyncgTTS import asyncgTTS
from .easygTTS import easygTTS

__all__ = ("setup", )

async def setup(premium: bool, *args, **kwargs):
    if not kwargs.get("session"):
        kwargs["session"] = ClientSession(raise_for_status=True)

    gtts = asyncgTTS if premium else easygTTS
    return gtts(*args, **kwargs)
