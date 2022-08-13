# Author: Adham Salama

from http.server import ThreadingHTTPServer
from typing import Callable
from pydantic import validate_arguments
from .request import Request
from .response import Response
from .custom_types import RouteHandler

HTTP_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]


class SimpleAPI:
    """
    SimpleAPI Class.

    Exposes HTTP methods to add routing and a method for running the app.
    """

    __request = Request

    def handle_request_decorator(self, path: str, method: str):
        def decorator(handler: Callable[[Request], Response]):

            handler_dict: RouteHandler = {
                "path": path,
                "method": method,
                "handler": handler,
            }
            self.__request.handlers.append(handler_dict)
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

    @validate_arguments
    def run(self, host: str = "localhost", port: int = 8000):
        web_server = ThreadingHTTPServer((host, port), self.__request)
        try:
            print("Server running at port", port)
            web_server.serve_forever()
        except KeyboardInterrupt:
            web_server.server_close()
            print("Server stopped")
