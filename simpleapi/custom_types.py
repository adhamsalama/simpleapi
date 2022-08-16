from __future__ import annotations
from typing import Callable, TypedDict
from .response import GenericResponse

ViewFunction = Callable[..., None]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
