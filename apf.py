# Author: Adham Salama

from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import json
from typing import Callable, TypedDict, Any
from pydantic import validate_arguments


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: Callable


HTTP_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]


class Request(BaseHTTPRequestHandler):
    handlers: list[RouteHandler] = []

    def json_response(self, code: int, data: Any):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), "utf-8"))

    def not_found(self):
        self.json_response(404, {"message": "Not found"})

    def handle_request(self, method: str):
        for handler in self.handlers:
            if handler["path"] == self.path and handler["method"] == method:
                return handler["handler"](self)
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
        def decorator(handler: Callable[[Request], None]):
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
