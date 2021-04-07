class LibraryException(Exception):
    "Base Error for entire asyncgTTS library"
    pass


class NoInitialisedSession(LibraryException):
    "Raised when no aiohttp session is available or creatable"
    pass

class RatelimitException(LibraryException):
    """Raised when getting a 418 response from Google

    Parameters:
        resp_content: Response body    as str
        resp_headers: Response headers as dict
    """

    def __init__(self, resp_content: str, resp_headers: dict, *args, **kwargs):
        self.resp_content = resp_content
        self.resp_headers = resp_headers

        super().__init__(*args, **kwargs)


class easygttsException(LibraryException):
    "Base Error for easygTTS code. (premium=False)"
    pass


class asyncgttsException(LibraryException):
    "Base Error for asyncgTTS code. (premium=True)"
    pass

class AuthorizationException(asyncgttsException):
    "Raised when getting a 401 response from Google"
    pass

class UnknownResponse(asyncgttsException):
    """Raised when getting an unknown JSON response from Google

    Parameters:
        resp: The unrecognisable JSON response decoded into a dictionary.
    """

    def __init__(self, resp: dict, *args, **kwargs):
        self.resp = resp

        super().__init__(*args, **kwargs)
