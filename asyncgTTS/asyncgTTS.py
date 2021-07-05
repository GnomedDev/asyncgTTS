from __future__ import annotations

import json
import time
from base64 import b64decode
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

import jwt
from aiohttp import ClientSession

from ._decos import require_session
from .errors import (AuthorizationException, RatelimitException,
                     UnknownResponse, asyncgttsException)
from .gtts import gtts


if TYPE_CHECKING:
    from typing_extensions import TypedDict

    class Voice(TypedDict):
        naturalSampleRateHertz: int
        languageCodes: List[str]
        ssmlGender: str
        name: str


GOOGLE_API_URL = "https://texttospeech.googleapis.com/"
class JSONWebTokenHandler:
    def __init__(self, service_account: Dict[str, str]) -> None:
        self.expire_time = 0.0
        self._jwt: Optional[str] = None

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
            jwt: str = jwt.decode()

        return jwt

    @property
    def jwt(self) -> str:
        jwt_token = self._jwt
        if not jwt_token or time() > self.expire_time:
            jwt_token = self.get_jwt()

        self._jwt = jwt_token
        return self._jwt

    def get_jwt(self) -> str:
        current_time = time.time()
        self.expire_time = current_time + 3600

        payload: Dict[str, Union[str, float]] = {}
        payload.update(self.partial_payload)
        payload.update(
            {
                "iat": current_time,
                "exp": self.expire_time
            }
        )

        jwt_token: str = jwt.encode(
            payload,
            self.pkey,
            headers=self.additional_headers,
            algorithm="RS256"
        )
        self._jwt = jwt_token
        return jwt_token

    refresh_jwt = get_jwt # backwards compatibility

class asyncgTTS(gtts):
    static_headers = {"Content-Type": "application/json; charset=utf-8"}
    def __init__(self,
        session: ClientSession,
        service_account_json_location: str = None
    ):
        if not service_account_json_location:
            raise AuthorizationException

        with open(service_account_json_location) as json_file:
            service_account = json.load(json_file)

        self.jwt = JSONWebTokenHandler(service_account)
        super().__init__(session)

    @property
    def headers(self) -> Dict[str, str]:
        # Handle loading of Bearer token.
        headers = {}
        headers.update(self.static_headers)
        headers.update({"Authorization": f"Bearer {self.jwt}"})

        return headers

    @require_session
    async def get(self,
        text: str,
        voice_lang: Tuple[str, str] = ("en-US-Standard-B", "en-us"),
        ret_type: str = "OGG_OPUS"
    ) -> bytes:

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

        async with self.session.post(
            f"{GOOGLE_API_URL}v1/text:synthesize",
            json=json_body, headers=self.headers
        ) as resp:
            if resp.ok:
                resp_json = await resp.json()
                try:
                    return b64decode(resp_json["audioContent"])
                except KeyError:
                    raise UnknownResponse(resp_json)

            elif resp.status == 401:
                raise AuthorizationException
            elif resp.status == 429:
                raise RatelimitException(await resp.text(), dict(resp.headers))

            raise asyncgttsException(
                f"{resp.status} {resp.reason}: {resp.content}"
            )

    @require_session
    async def get_voices(self) -> List[Voice]:
        async with self.session.get(f"{GOOGLE_API_URL}v1/voices", headers=self.headers) as resp:
            return (await resp.json())["voices"]
