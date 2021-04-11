from aiohttp import ClientSession

from ._decos import require_session
from .errors import RatelimitException, easygttsException
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

        async with self.session.get(f"{self.url}v1/tts", params=kwargs) as resp:
            if resp.ok:
                return await resp.read()

            elif resp.status == 429:
                content = await resp.text()
                headers = dict(resp.headers)

                raise RatelimitException(content, headers)

            else:
                raise easygttsException(f"{resp.status} {resp.reason}: {resp.content}")

    @require_session
    async def langs(self):
        async with self.session.get(f"{self.url}v1/langs") as resp:
            return await resp.json()
