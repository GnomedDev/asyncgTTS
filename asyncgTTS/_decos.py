class NoContextManagerException(Exception): pass

def require_session(func):
    async def wrapper(self, *args, **kwargs):
        if self.session:
            return await func(*args, **kwargs)

        raise NoContextManagerException("Session is not initialized, use context manager or pass aiohttp.ClientSession on init")

    return wrapper
