__version__ = "0.1.1"

from .custom_types import RouteHandler, ViewFunction, Middleware
from .request import Request
from .response import (
    ErrorResponse,
    JSONResponse,
    NotFoundErrorResponse,
    Response,
    ValidationErrorResponse,
)
from .router import Router
from .simpleapi import SimpleAPI

# ? Resources

# https://wsgi.readthedocs.io/en/latest/definitions.html

# https://wsgi.readthedocs.io/en/latest/specifications/handling_post_forms.html

# https://www.toptal.com/python/pythons-wsgi-server-application-interface

# https://peps.python.org/pep-3333/

# https://docs.gunicorn.org/en/stable/
