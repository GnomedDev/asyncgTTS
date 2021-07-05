from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, cast

from .errors import NoInitialisedSession


if TYPE_CHECKING:
    from typing import TypeVar
    from typing_extensions import ParamSpec

    _R = TypeVar("_R")
    _P = ParamSpec("_P")


def require_session(func: Callable[_P, _R]) -> Callable[_P, _R]:
    @wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        self = cast(Any, args[0])

        if self.session:
            return func(*args, **kwargs)

        raise NoInitialisedSession("Session is not initialized, use async context manager or pass aiohttp.ClientSession on init")
    return wrapper
