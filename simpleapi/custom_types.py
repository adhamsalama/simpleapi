from __future__ import annotations
from typing import Callable, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .request import Request
from .response import Response

ViewFunction = Callable[..., Response]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
