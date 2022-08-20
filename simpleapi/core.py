from typing import Any

from .custom_types import Middleware, RouteHandler, ViewFunction


class API:
    """
    Core API

    Exposes HTTP methods to add routing and a method for running the app.
    """

    def __init__(self, middleware: list[Middleware] | None = None) -> None:
        self.handlers: list[RouteHandler] = []
        self.body: dict[str, Any] = {}
        self.extra: dict[Any, Any] = {}  # Extra dict for middleware to attach data to
        self.query: dict[Any, list[str]] = {}
        self.params: dict[str, str] = {}
        self.middleware: list[Middleware] = middleware if middleware else []

    def handle_request_decorator(
        self, path: str, method: str, middleware: list[Middleware] | None
    ):
        def decorator(handler: ViewFunction):

            handler_dict: RouteHandler = {
                "path": path,
                "method": method,
                "handler": handler,
                "middleware": middleware if middleware else [],
                "router_id": id(self),
            }
            self.handlers.append(handler_dict)
            return handler

        return decorator

    def get(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "GET", middleware)

    def post(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "POST", middleware)

    def put(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "PUT", middleware)

    def patch(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "PATCH", middleware)

    def delete(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "DELETE", middleware)

    def head(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "HEAD", middleware)

    def options(self, path: str, middleware: list[Middleware] | None = None):
        return self.handle_request_decorator(path, "OPTIONS", middleware)
