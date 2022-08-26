from typing import Any

from . import utils


class Request:
    """HTTP Request"""

    def __init__(self, environ: utils.Environ) -> None:
        self.environ = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.extra: dict[str, Any] = {}
        self.params: dict[str, str] = {}
        self.form: dict[str, bytes]
        self.body: dict[str, str | int | float | bool | dict]
        self.body, self.form = utils.parse_body(environ)
        self.query = utils.parse_query_string(environ)
        self.headers: dict[str, str] = utils.parse_headers(environ)
        self.cookies: dict[str, str] = utils.parse_cookies(environ)
