from __future__ import annotations
from typing import Callable, TypedDict
from .response import GenericResponse, Response

ViewFunction = Callable[..., Response]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
