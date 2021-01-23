from base64 import b64decode
from typing import Dict, List, Tuple, Union

from aiohttp import ClientSession

from ._decos import require_session
from .gtts import gtts


class NoContextManagerException(Exception): pass
GOOGLE_API_URL = "https://texttospeech.googleapis.com/v1/"

class asyncgTTS(gtts):
    def __init__(self, session: ClientSession, auth_token: Union[str, bytes]):
        self.voices = None
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {auth_token}"
        }

        super().__init__(session)

    def require_session(func):
        async def wrapper(self, *args, **kwargs):
            if self.session:
                return await func(self, *args, **kwargs)

            raise NoContextManagerException("Session is not initialized, use context manager or pass aiohttp.ClientSession on init")

        return wrapper

    @require_session
    async def get(self, text: str, voice_lang: Tuple[str] = ("en-US-Standard-B", "en-us"), ret_type: str = "OGG_OPUS") -> bytes:
        json_body = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": voice_lang[-1],
                "name": voice_lang[0],
            },
            "audioConfig": {
                "audioEncoding": ret_type
            }
        }

        async with self.session.post(f"{GOOGLE_API_URL}text:synthesize", json=json_body, headers=self.headers) as resp:
            audio_json = await resp.json()
            return b64decode(audio_json["audioContent"])

    @require_session
    async def get_voices(self) -> List[dict]:
        async with self.session.get(f"{GOOGLE_API_URL}voices", headers=self.headers) as resp:
            return (await resp.json())["voices"]
