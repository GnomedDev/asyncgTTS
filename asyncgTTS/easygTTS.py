from aiohttp import ClientSession

from ._decos import require_session
from .gtts import gtts


OFFICIAL_URL = "http://easy-gtts.herokuapp.com/"

class easygTTS(gtts):
    def __init__(self, session: str = ClientSession, base_url: str = OFFICIAL_URL):
        self.url = base_url
        super().__init__(session)

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
