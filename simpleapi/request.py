import cgi
import json
from typing import Any
from typing import BinaryIO, Callable, TypedDict

from .response import GenericResponse


Environ = TypedDict(
    "Environ",
    {
        "REQUEST_METHOD": str,
        "SCRIPT_NAME": str,
        "PATH_INFO": str,
        "QUERY_STRING": str,
        "CONTENT_TYPE": str,
        "CONTENT_LENGTH": str,
        "SERVER_NAME": str,
        "SERVER_PORT": int,
        "SERVER_PROTOCOL": str,
        "HTTP_": list[str],
        "wsgi.version": tuple[int, int],
        "wsgi.url_scheme": str,
        "wsgi.input": BinaryIO,
        "wsgi.errors": BinaryIO,
        "wsgi.multithread": bool,
        "wsgi.multiprocess": bool,
        "wsgi.run_once": bool,
    },
)


class Request:
    """HTTP Request"""

    def __init__(self, environ: Environ) -> None:
        self.environ = environ
        body = environ["wsgi.input"]
        self.form: dict[str, bytes] = {}
        if is_post_request(environ):
            storage = cgi.FieldStorage(fp=body, environ=environ)  # type: ignore
            self.body: dict[str, str | int | float | bool] = {}
            for k in storage.keys():
                self.form[k] = storage[k].value
        else:
            read_body = body.read()
            self.body = json.loads(read_body) if read_body else {}
        self.method = environ["REQUEST_METHOD"]
        self.query = parse_query_string(environ["QUERY_STRING"])
        self.path = environ["PATH_INFO"]
        self.extra: dict[str, Any] = {}
        self.params: dict[str, str] = {}


def is_post_request(environ: Environ):
    if environ["REQUEST_METHOD"].upper() != "POST":
        return False
    content_type = environ.get("CONTENT_TYPE", "application/x-www-form-urlencoded")
    return content_type.startswith(
        "application/x-www-form-urlencoded"
    ) or content_type.startswith("multipart/form-data")


def parse_query_string(qs: str) -> dict[str, str]:
    # ? I have decided to save only one value instead of an array of values
    if not qs:
        return {}
    qs_list = qs.split("&")
    result: dict[str, str] = {}
    for q in qs_list:
        equal_index = q.index("=")
        key = q[:equal_index]
        value = q[equal_index + 1 :]
        result[key] = value
    return result
