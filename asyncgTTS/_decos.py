from .errors import NoInitialisedSession

def require_session(func):
    async def wrapper(self, *args, **kwargs):
        if self.session:
            return await func(self, *args, **kwargs)

        raise NoInitialisedSession("Session is not initialized, use async context manager or pass aiohttp.ClientSession on init")

    return wrapper
