from aiohttp import ClientSession

from ._decos import require_session
from .gtts import gtts


class NoContextManagerException(Exception): pass
offical_url = "http://easy-gtts.herokuapp.com/"

class easygTTS(gtts):
    def __init__(self, session: str = ClientSession, base_url: str = offical_url):
        self.url = base_url
        super().__init__(session)

    def require_session(func):
        async def wrapper(self, *args, **kwargs):
            if self.session:
                return await func(self, *args, **kwargs)

            raise NoContextManagerException("Session is not initialized, use context manager or pass aiohttp.ClientSession on init")

        return wrapper

    @require_session
    async def get(self, **kwargs):
        if not kwargs.get("lang"):
            kwargs["lang"] = "en"

        async with self.session.get(f"{self.url}tts", params=kwargs) as resp:
            return await resp.read()

    @require_session
    async def langs(self):
        async with self.session.get(f"{self.url}langs") as resp:
            return await resp.json()
