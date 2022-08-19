from typing import Any

from .custom_types import RouteHandler, ViewFunction


class API:
    """
    Core API

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
