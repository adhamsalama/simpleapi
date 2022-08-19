# Author: Adham Salama

import json
from typing import Callable

from .core import API
from .custom_types import Environ
from .handler import handle_request
from .request import Request
from .response import WSGIResponse
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
