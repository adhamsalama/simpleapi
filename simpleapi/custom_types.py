from typing import BinaryIO, Callable, TypedDict

from simpleapi.request import Request

from .response import GenericResponse


ViewFunction = Callable[..., GenericResponse]
Middleware = Callable[[Request], None]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
    middleware: list[Middleware]
