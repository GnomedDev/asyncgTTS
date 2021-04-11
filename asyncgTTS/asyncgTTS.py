import json
from base64 import b64decode
from time import time
from typing import Dict, List, Tuple, Union

import jwt
from aiohttp import ClientSession

from ._decos import require_session
from .errors import (AuthorizationException, RatelimitException,
                     UnknownResponse, asyncgttsException)
from .gtts import gtts

GOOGLE_API_URL = "https://texttospeech.googleapis.com/"


class JSONWebTokenHandler:
    def __init__(self, service_account: dict) -> None:
        self._jwt = None
        self.expire_time = 0.0

        service_account_email = service_account["client_email"]
        self.partial_payload = {
            "aud": GOOGLE_API_URL,
            "iss": service_account_email,
            "sub": service_account_email,
            }

        self.pkey = service_account["private_key"]
        self.additional_headers = {"kid": self.pkey}

    def __str__(self):
        jwt = self.jwt
        if isinstance(jwt, bytes):
            jwt = jwt.decode()

        return jwt

    @property
    def jwt(self):
        if time() > self.expire_time:
            self.refresh_jwt()

        return self._jwt

    def refresh_jwt(self):
        current_time = time()
        self.expire_time = current_time + 3600

        payload = {}
        payload.update(self.partial_payload)
        payload.update(
            {
                "iat": current_time,
                "exp": self.expire_time
            }
        )

        self._jwt = jwt.encode(
            payload,
            self.pkey,
            headers=self.additional_headers,
            algorithm="RS256"
        )

class asyncgTTS(gtts):
    def __init__(self, session: ClientSession, service_account_json_location: str = None):
        if not service_account_json_location:
            raise AuthorizationException

        with open(service_account_json_location) as json_file:
            service_account = json.load(json_file)

        self.jwt = JSONWebTokenHandler(service_account)
        super().__init__(session)

    static_headers = {"Content-Type": "application/json; charset=utf-8"}

    @property
    def headers(self):
        # Handle loading of Bearer token.
        headers = {}
        headers.update(self.static_headers)
        headers.update({"Authorization": f"Bearer {self.jwt}"})

        return headers

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

        async with self.session.post(f"{GOOGLE_API_URL}v1/text:synthesize", json=json_body, headers=self.headers) as resp:
            if resp.ok:
                resp_json = await resp.json()
                try:
                    audio_data = b64decode(resp_json["audioContent"])
                    return audio_data
                except KeyError:
                    raise UnknownResponse(resp_json)

            elif resp.status == 401:
                raise AuthorizationException

            elif resp.status == 429:
                content = resp.content
                headers = dict(resp.headers)

                raise RatelimitException(content, headers)

            else:
                raise asyncgttsException(f"{resp.status} {resp.reason}: {resp.content}")

    @require_session
    async def get_voices(self) -> List[dict]:
        async with self.session.get(f"{GOOGLE_API_URL}v1/voices", headers=self.headers) as resp:
            return (await resp.json())["voices"]
