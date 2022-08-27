import cgi
import json
from typing import BinaryIO, TypedDict

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
        "HTTP_COOKIE": str,
        "wsgi.version": tuple[int, int],
        "wsgi.url_scheme": str,
        "wsgi.input": BinaryIO,
        "wsgi.errors": BinaryIO,
        "wsgi.multithread": bool,
        "wsgi.multiprocess": bool,
        "wsgi.run_once": bool,
    },
)


def is_form_data_request(environ: Environ) -> bool:
    """Returns True of the request method is POST, False otherwise"""
    if environ["REQUEST_METHOD"].upper() != "POST":
        return False
    content_type = environ.get("CONTENT_TYPE", "application/x-www-form-urlencoded")
    return content_type.startswith(
        "application/x-www-form-urlencoded"
    ) or content_type.startswith("multipart/form-data")


def parse_body(
    environ: Environ,
) -> tuple[dict[str, str | int | float | bool | dict], dict[str, bytes]]:
    """Parses request body and form data"""
    raw_body = environ["wsgi.input"]
    body: dict[str, str | int | float | bool | dict] = {}
    form: dict[str, bytes] = {}
    if is_form_data_request(environ):
        storage = cgi.FieldStorage(fp=raw_body, environ=environ)  # type: ignore
        body = {}
        for k in storage.keys():
            form[k] = storage[k].value
    else:
        read_body = raw_body.read()
        body = json.loads(read_body) if read_body else {}
    return body, form


def parse_query_string(environ: Environ) -> dict[str, str]:
    """Parses query parameters from a query string and returns a dict"""
    # ? I have decided to save only one value instead of an array of values
    if not environ["QUERY_STRING"]:
        return {}
    return {
        k: v
        for [k, v] in [query.split("=") for query in environ["QUERY_STRING"].split("&")]
    }


def parse_cookies(environ: Environ) -> dict[str, str]:
    """Parses cookies from a cookie string and returns a dict of cookies, with keys as lowercase"""
    # God, I love list/dict/set comprehension!
    return (
        {
            k: v
            for [k, v] in [
                [
                    cookie[: cookie.index("=")],
                    cookie[cookie.index("=") + 1 :],
                ]  # Fix bug where cookie value contains "="
                for cookie in environ["HTTP_COOKIE"].replace(" ", "").split(";")
            ]
        }
        if "HTTP_COOKIE" in environ.keys()
        else {}
    )


def parse_headers(environ: Environ) -> dict[str, str]:
    """Parses headers from a request and returns a dict of headers"""
    headers: dict[str, str] = {}
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            headers[k.strip("HTTP_").lower()] = v  # type: ignore
    return headers
