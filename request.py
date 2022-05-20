from http.server import BaseHTTPRequestHandler
import json
from response import Response, RouteHandler


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
