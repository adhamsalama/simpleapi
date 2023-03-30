from typing import Callable, TypedDict

from simpleapi.request import Request

from .response import GenericResponse, Response

ViewFunction = Callable[..., GenericResponse]
Middleware = Callable[[Request], Response | None]
ComponentMiddleware = dict[int, list[Middleware]]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
    middleware: list[Middleware]
    router_id: int


class Query:
    def __init__(self, query: str) -> None:
        self.key = query
        self.value: str | list[str] = None  # type: ignore
