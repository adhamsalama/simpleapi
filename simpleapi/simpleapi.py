# Author: Adham Salama

import json
from typing import Callable

from .core import API
from .custom_types import ComponentMiddleware, Middleware, RouteHandler, ViewFunction
from .handler import handle_request
from .request import Request
from .response import ParsingErrorResponse, WSGIResponse
from .router import Router
from .utils import Environ


class SimpleAPI(API):
    """
    SimpleAPI Class.
    """

    def __init__(self, middleware: list[Middleware] | None = None) -> None:
        self.component_middleware: ComponentMiddleware = {
            1: middleware if middleware else []
        }

        super().__init__(middleware if middleware else [])

    # ? Override handle_request_decorator to make the component_id = 1 for global app middleware
    def handle_request_decorator(
        self, path: str, method: str, middleware: list[Middleware] | None
    ):
        def decorator(handler: ViewFunction):

            handler_dict: RouteHandler = {
                "path": path,
                "method": method,
                "handler": handler,
                "middleware": middleware if middleware else [],
                "router_id": 1,
            }
            self.handlers.append(handler_dict)
            return handler

        return decorator

    def add_router(self, prefix: str, router: Router):
        # Add component middleware
        self.component_middleware[id(router)] = router.middleware
        # Add handlers middleware
        for handler in router.handlers:
            handler["path"] = prefix + handler["path"]
            self.handlers.append(handler)

    def __call__(self, environ: Environ, start_response: Callable):
        try:
            request = Request(environ=environ)
            response = handle_request(
                request=request,
                handlers=self.handlers,
                app_middleware=self.component_middleware,
            )
        except json.decoder.JSONDecodeError:
            response = ParsingErrorResponse()
        wsgi_response = WSGIResponse.simple_response(start_response, response)
        return wsgi_response.send()
