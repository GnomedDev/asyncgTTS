from typing import Literal, Optional, Union, overload
from aiohttp import ClientSession

from .asyncgTTS import asyncgTTS
from .easygTTS import easygTTS
from .errors import *

__all__ = ("setup", )

@overload
async def setup(
    premium: Literal[True],
    session: Optional[ClientSession],
    service_account_json_location: str
) -> asyncgTTS: ...
@overload
async def setup(
    premium: Literal[False],
    session: Optional[ClientSession],
    base_url: Optional[str]
) -> easygTTS: ...

async def setup(premium: bool, *args, **kwargs) -> Union[asyncgTTS, easygTTS]:
    if not kwargs.get("session"):
        kwargs["session"] = ClientSession()

    gtts = asyncgTTS if premium else easygTTS
    return gtts(*args, **kwargs)
