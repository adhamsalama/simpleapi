from typing import Callable, TypedDict

from simpleapi.request import Request

from .response import GenericResponse

ViewFunction = Callable[..., GenericResponse]
Middleware = Callable[[Request], None]
ComponentMiddleware = dict[int, list[Middleware]]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
    middleware: list[Middleware]
    router_id: int
