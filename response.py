import json
from typing import Any, Callable, TypedDict
from pydantic import validate_arguments, BaseModel, Field


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


class JSONResponse(Response):
    content_type: str = "application/json"

    def parse_message(self):
        return json.dumps(self.message)


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: Callable[[Any], Response]
