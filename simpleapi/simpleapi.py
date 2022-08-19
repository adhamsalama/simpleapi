# Author: Adham Salama

import json

from .custom_types import Environ
from .request import Request
from .response import WSGIResponse

from .custom_types import RouteHandler, ViewFunction, Environ
from .request import Request
from typing import Any, Callable
from .handler import handle_request

# def app(environ: Environ, start_response):

#     request = Request(environ=environ)
#     print(request.method,request.body, request.query, environ["SCRIPT_NAME"], environ["PATH_INFO"])
#     # body = b"Hello world!\n"
#     # status = "200 OK"
#     # headers = [("Content-type", "text/plain")]
#     # start_response(status, headers)
#     # return [body]
#     response = WSGIResponse(start_response,status="200 OK", headers=[("Content-type", "text/plain")])
#     return response.send([b"Hello world!\n"])


HTTP_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]


class SimpleAPI:
    """
    SimpleAPI Class.

    Exposes HTTP methods to add routing and a method for running the app.
    """

    def __init__(self) -> None:
        self.handlers: list[RouteHandler] = []
        self.body: dict[str, Any] = {}
        self.extra: dict[Any, Any] = {}  # Extra dict for middleware to attach data to
        self.query: dict[Any, list[str]] = {}
        self.params: dict[str, str] = {}

    def handle_request_decorator(self, path: str, method: str):
        def decorator(handler: ViewFunction):

            handler_dict: RouteHandler = {
                "path": path,
                "method": method,
                "handler": handler,
            }
            self.handlers.append(handler_dict)
            return handler

        return decorator

    def get(self, path: str):
        return self.handle_request_decorator(path, "GET")

    def post(self, path: str):
        return self.handle_request_decorator(path, "POST")

    def put(self, path: str):
        return self.handle_request_decorator(path, "PUT")

    def patch(self, path: str):
        return self.handle_request_decorator(path, "PATCH")

    def delete(self, path: str):
        return self.handle_request_decorator(path, "DELETE")

    def head(self, path: str):
        return self.handle_request_decorator(path, "HEAD")

    def options(self, path: str):
        return self.handle_request_decorator(path, "OPTIONS")

    def __call__(self, environ: Environ, start_response: Callable):
        request = Request(environ=environ)
        response = handle_request(request=request, handlers=self.handlers)
        response.headers.append(("content-type", response.content_type))
        wsgi_response = WSGIResponse(start_response, status=str(response.code), headers=response.headers)
        if isinstance(response.body, bytes):
            return wsgi_response.send(response.body)
        elif isinstance(response.body, dict):
            return wsgi_response.send(bytes(json.dumps(response.body, indent=2).encode("utf-8")))
        else:
            return wsgi_response.send(response.body.encode())
