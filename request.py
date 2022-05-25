import cgi
from http.server import BaseHTTPRequestHandler
import json
from typing import Any
from response import Response
from custom_types import RouteHandler
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

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps("Not found"), "utf-8"))

    def handle_request(self, method: str):
        """
        A method that tries to find the matching route handler.
        Extra code for handling POST requests is done in its own function because it's a bit more complex.
        """
        for handler in self.handlers:
            if handler["path"] == self.path and handler["method"] == method:
                response: Response = handler["handler"](self)
                # Add status code
                self.send_response(response.code)
                # Add content type
                self.send_header("Content-type", response.content_type)
                # Add headers
                for header in response.headers:
                    self.send_header(header[0], header[1])
                self.end_headers()
                if response.message is not None:
                    self.wfile.write(bytes(response.parse_message(), response.encoding))
                return
        self.not_found()

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        # Handle post request body types
        # Originally from
        # https://stackoverflow.com/questions/17690585/how-do-i-access-the-data-sent-to-my-server-using-basehttprequesthandler
        # Had to modify it a bit to work
        for handler in self.handlers:
            if handler["path"] == self.path and handler["method"] == "POST":
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
                # The rest is the same as handling any other request
                return self.handle_request("POST")
        self.not_found()

    def do_PUT(self):
        self.handle_request("PUT")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def HEAD(self):
        self.handle_request("HEAD")

    def do_OPTIONS(self):
        self.handle_request("OPTIONS")
