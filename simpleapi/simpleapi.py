# Author: Adham Salama

import json
from typing import Callable

from .core import API
from .custom_types import Environ
from .handler import handle_request
from .request import Request
from .response import ParsingErrorResponse, WSGIResponse
from .router import Router

HTTP_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]


class SimpleAPI(API):
    """
    SimpleAPI Class.
    """

    def add_router(self, prefix: str, router: Router):
        for handler in router.handlers:
            handler["path"] = prefix + handler["path"]
            self.handlers.append(handler)

    def __call__(self, environ: Environ, start_response: Callable):
        try:
            request = Request(environ=environ)
            response = handle_request(request=request, handlers=self.handlers)
        except json.decoder.JSONDecodeError:
            response = ParsingErrorResponse()
        wsgi_response = WSGIResponse.simple_response(start_response, response)
        return wsgi_response.send()
