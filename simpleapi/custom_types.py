from __future__ import annotations

from typing import TypedDict, BinaryIO, ByteString
from typing import Callable, TypedDict
from .response import GenericResponse

Environ = TypedDict("Environ", {
    "REQUEST_METHOD": str,
    "SCRIPT_NAME": str,
    "PATH_INFO": str,
    "QUERY_STRING": str,
    "CONTENT_TYPE": str,
    "CONTENT_LENGTH": str,
    "SERVER_NAME": str,
    "SERVER_PORT": int,
    "SERVER_PROTOCOL": str,
    "HTTP_": list[str],
    "wsgi.version": tuple[int, int],
    "wsgi.url_scheme": str,
    "wsgi.input": BinaryIO,
    "wsgi.errors": BinaryIO,
    "wsgi.multithread": bool,
    "wsgi.multiprocess": bool,
    "wsgi.run_once": bool
})


ViewFunction = Callable[..., GenericResponse]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
