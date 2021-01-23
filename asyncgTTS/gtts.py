import aiohttp

from ._decos import require_session


class gtts:
    def __init__(self, session: aiohttp.ClientSession = None):
        self.used_session = None
        self.passed_session = session

    async def __aenter__(self):
        self.used_session = self.passed_session or aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.used_session.close()

    @property
    def session(self):
        a = self.passed_session or self.used_session
        return a

    async def close(self):
        for session in (self.used_session, self.passed_session):
            if session:
                await session.close()

    @require_session
    async def get(self, *args, **kwargs):
        raise NotImplementedError
