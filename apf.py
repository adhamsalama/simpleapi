# Author: Adham Salama

from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import json
from typing import Callable, TypedDict, Any, Annotated, get_type_hints
from pydantic import validate_arguments, BaseModel, Field


HTTP_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]


class Response(BaseModel):
    """
    HTTP Response Class.

    This should be used instead of using the Request class directly.

    Properties:
        code: Response status code, default = 200
        message: Response body
        headers: Response headers
        content_type: Response content-type
        encoding: Response encoding
        parse_message: Parses the message into the correct format
    """

    code: int = Field(default=200, ge=100, le=599)
    message: Any
    headers: list[tuple[str, str]] = []
    content_type: str
    encoding: str = Field(default="utf-8")

    @validate_arguments
    def set_header(self, header: str, value: str) -> None:
        self.headers.append((header, value))

    def parse_message(self):
        return self.message


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: Callable[[Any], Response]


class JSONResponse(Response):
    content_type: str = "application/json"

    def parse_message(self):
        return json.dumps(self.message)


class Request(BaseHTTPRequestHandler):
    """
    HTTP Request.
    """

    # TODO: I should somehow make these methods not acceessible from views
    # TODO: Add dynamic routing
    # TODO: Allow view functions to return dicts and pydantic classes and auto-serialize them

    handlers: list[RouteHandler] = []

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"message": "Not found"}), "utf-8"))

    def handle_request(self, method: str):
        """
        A method that tries to find the matching route handler.
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
                self.wfile.write(bytes(response.parse_message(), response.encoding))
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


class APF:
    def handle_request_decorator(self, path: str, method: str):
        def decorator(handler: Callable[[Request], Response]):

            handler_dict: RouteHandler = {
                "path": path,
                "method": method,
                "handler": handler,
            }
            Request.handlers.append(handler_dict)
            return handler

        return decorator

    def get(self, path: str):
        return self.handle_request_decorator(path, "GET")

    def post(self, path: str):
        return self.handle_request_decorator(path, "POST")

    def put(self, path: str):
        return self.handle_request_decorator(path, "PUT")

    def patch(self, path: str):
        return self.handle_request_decorator(path, "PATCH")

    def delete(self, path: str):
        return self.handle_request_decorator(path, "DELETE")

    def head(self, path: str):
        return self.handle_request_decorator(path, "HEAD")

    def options(self, path: str):
        return self.handle_request_decorator(path, "OPTIONS")

    @validate_arguments
    def run(self, host: str, port: int, multithreading: bool = False):
        if multithreading:
            web_server = HTTPServer((host, port), Request)
        else:
            web_server = ThreadingHTTPServer((host, port), Request)
        try:
            print("Server running at port", port)
            web_server.serve_forever()
        except KeyboardInterrupt:
            web_server.server_close()
            print("Server stopped")
