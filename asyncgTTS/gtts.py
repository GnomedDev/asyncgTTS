from __future__ import annotations
from typing import Optional

import aiohttp

from ._decos import require_session


class gtts:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.passed_session = session

    async def __aenter__(self) -> gtts:
        self.used_session = self.passed_session or aiohttp.ClientSession()
        return self

    async def __aexit__(self, *_) -> None:
        await self.used_session.close()

    @property
    def session(self):
        return self.passed_session or self.used_session

    async def close(self):
        for session in (self.used_session, self.passed_session):
            if session:
                await session.close()


    @require_session
    async def get(self, *args, **kwargs):
        raise NotImplementedError
