from typing import Any

from . import utils


class Request:
    """
    HTTP Request

    Properties:
    environ (The WSGI environ).
    method (The request HTTP method)
    path (The request path).
    params (The route's dynamic parameters).
    form (The request body's form data).
    body (The request's JSON body).
    query (The request's query parameters).
    headers (The request's headers).
    cookies (The requests's cookies).
    extra (A dict to which middleware can add fields).
    """

    def __init__(self, environ: utils.Environ) -> None:
        self.method: str = environ["REQUEST_METHOD"]
        self.path: str = environ["PATH_INFO"]
        self.extra: dict[str, Any] = {}
        self.params: dict[str, str] = {}
        self.form: dict[str, bytes]
        self.body: dict[str, str | int | float | bool | dict]
        self.body, self.form = utils.parse_body(environ)
        self.query = utils.parse_query_string(environ)
        self.headers: dict[str, str] = utils.parse_headers(environ)
        self.cookies: dict[str, str] = utils.parse_cookies(environ)
