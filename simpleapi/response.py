import json
from typing import Any, Callable, TypeVar

from pydantic import BaseModel, Field, validate_arguments


start_response_function = Callable[[str, list[tuple[str, str]]], Any]

class WSGIResponse:
    def __init__(self, start_response: start_response_function, status: str, headers: list[tuple[str, str]]) -> None:
        start_response(status, headers)
    def send(self, body: bytes | dict[str, Any] | str):
        return [body]



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
    body: Any
    code: int = Field(default=200, ge=100, le=599)
    headers: list[tuple[str, str]] = []
    content_type: str
    encoding: str = Field(default="utf-8")

    @validate_arguments
    def set_header(self, header: str, value: str) -> None:
        self.headers.append((header, value))

    def parse_body(self):
        return self.body


class JSONResponse(Response):
    content_type: str = "application/json"

    def parse_body(self):
        return json.dumps(self.body)


GenericResponse = TypeVar("GenericResponse", Response, str, int, float, BaseModel, dict)
