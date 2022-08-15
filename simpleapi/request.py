import cgi
from http.server import BaseHTTPRequestHandler
import json
from typing import Any, get_type_hints
from .response import JSONResponse, Response, GenericResponse
from .custom_types import RouteHandler
from urllib import parse


class Request(BaseHTTPRequestHandler):
    """
    HTTP Request.
    """

    # TODO: I should somehow make these methods not acceessible from views
    # TODO: Add dynamic routing
    # TODO: Allow view functions to return dicts and pydantic classes and auto-serialize them

    handlers: list[RouteHandler] = []
    body: dict[str, Any] = {}
    extra: dict[Any, Any] = {}  # Extra dict for middleware to attach data to
    query: dict[Any, list[str]] = {}
    params: dict[str, str] = {}

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps("Not found"), "utf-8"))

    def handle_request(self, method: str):
        """
        A method that tries to find the matching route handler.
        """
        # Parse query params
        if "?" in self.path:
            self.query = parse.parse_qs(self.path[self.path.index("?") + 1 :], keep_blank_values=True)  # type: ignore
            # Remove them from path
            self.path = self.path[: self.path.index("?")]
        for handler in self.handlers:
            # ? Check dynamic routes
            is_dynamic = False
            if "{" in handler["path"] and "}" in handler["path"]:  # ['/greet/{name}']
                # ? Ignore first slash
                # ! This wont work for trailing backslash
                handler_path = handler["path"].split("/")[
                    1:
                ]  # path = ['greet', '{name}']
                request_path = self.path.split("/")[1:]
                if len(handler_path) == len(request_path):
                    is_dynamic = True
                    for handler_part, request_part in zip(handler_path, request_path):
                        if (
                            handler_part[0] == "{" and handler_part[-1] == "}"
                        ):  # handler_part = '{name}'
                            self.params[handler_part[1:-1]] = request_part
            if handler["method"] == method and (
                handler["path"] == self.path or is_dynamic
            ):
                if method == "POST":
                    # Handle post request body types
                    # Originally from
                    # https://stackoverflow.com/questions/17690585/how-do-i-access-the-data-sent-to-my-server-using-basehttprequesthandler
                    # Had to modify it a bit to work
                    ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
                    if ctype == "multipart/form-data":
                        pdict["boundary"] = bytes(pdict["boundary"], "utf-8")  # type: ignore
                        self.body = cgi.parse_multipart(self.rfile, pdict)  # type: ignore
                        # parse_multipart returns an array of values for each key word
                        # I will only keep the first value
                        for k, v in self.body.items():
                            self.body[k] = v[0]
                    elif ctype == "application/x-www-form-urlencoded":
                        length = int(self.headers.get("content-length", 0))
                        self.body = parse.parse_qs(
                            self.rfile.read(length), keep_blank_values=True  # type: ignore
                        )
                    else:
                        # ! Assumes request body type is JSON
                        content_length = int(self.headers.get("Content-Length"), 0)
                        self.body = json.loads(self.rfile.read(content_length))

                handler_type_hints = get_type_hints(handler["handler"])
                dependency_injection: dict[str, Any] = {}
                for k, v in handler_type_hints.items():
                    if v == Request:
                        dependency_injection[k] = self
                response = handler["handler"](**dependency_injection)
                if isinstance(response, str):
                    constructed_response = Response(
                        code=200, message=response, content_type="string"
                    )
                elif isinstance(response, (int, float)):
                    constructed_response = Response(
                        code=200, message=str(response), content_type="string"
                    )
                elif isinstance(response, JSONResponse):
                    constructed_response = response
                elif isinstance(response, Response):
                    constructed_response = response
                else:
                    # Pydantic BaseModel
                    constructed_response = Response(
                        code=200,
                        message=response.json(),
                        content_type="application/json",
                    )

                # Add status code
                self.send_response(constructed_response.code)
                # Add content type
                self.send_header("Content-type", constructed_response.content_type)
                # Add headers
                for header in constructed_response.headers:
                    self.send_header(header[0], header[1])
                self.end_headers()
                if constructed_response.message is not None:
                    _response_message = constructed_response.parse_message()
                    if isinstance(_response_message, str):
                        self.wfile.write(bytes(_response_message, encoding="utf-8"))
                    else:
                        self.wfile.write(bytes(_response_message))
                return
        self.not_found()

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def HEAD(self):
        self.handle_request("HEAD")

    def do_OPTIONS(self):
        self.handle_request("OPTIONS")
