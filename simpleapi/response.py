import json
from typing import Any, Callable, TypedDict

from pydantic import BaseModel


class Error(TypedDict):
    loc: list[str]
    msg: str


class ErrorMessage(TypedDict):
    """
    Error Message Dict

    message: str
    field: str | None
    """

    errors: list[Error]


class Response:
    """
    HTTP Response.

    Properties:
        code: Response status code, default = 200
        message: Response body
        headers: Response headers
        content_type: Response content-type, default = text/html; charset=UTF-8"
    """

    def __init__(
        self,
        body: str | dict[str, Any] | list | bytes | ErrorMessage,
        content_type: str = "text/html; charset=UTF-8",
        headers: list[tuple[str, str]] | None = None,
        code: int = 200,
    ) -> None:
        # ? If the developer should set the content-type using the content_type argument and not supply it again to the headers argument
        self.body: Any = body
        self.content_type: str = content_type
        self.headers: list[tuple[str, str]] = headers if headers else []
        self.headers.append(("content-type", content_type))
        self.code = code

    def set_header(self, header: str, value: str) -> None:
        self.headers.append((header, value))

    def set_cookie(self, key: str, value: str):
        self.set_header("Set-Cookie", f"{key}={value}")


class JSONResponse(Response):
    # content_type: str = "application/json"
    def __init__(
        self,
        body: Any,
        headers: list[tuple[str, str]] | None = None,
        code: int = 200,
    ) -> None:
        super().__init__(
            code=code,
            body=body,
            content_type="application/json",
            headers=headers if headers else [],
        )


class ErrorResponse(Response):
    """
    Base Class for Errors

    # Status Code
    code: int
    # Error Messages
    messages: list[ErrorMessage]
    """

    def __init__(self, messages: ErrorMessage, code: int = 500) -> None:
        self.code: int = code
        self.messages: ErrorMessage = messages
        super().__init__(
            code=self.code,
            body=self.messages,
            content_type="application/json",
            headers=[],
        )


class ValidationErrorResponse(ErrorResponse):
    """Error Response for Validation"""

    def __init__(self, messages: ErrorMessage) -> None:
        self.code = 403
        self.messages: ErrorMessage = messages
        super().__init__(code=self.code, messages=self.messages)


class NotFoundErrorResponse(ErrorResponse):
    """Error Response for Not Found"""

    def __init__(
        self,
        messages: ErrorMessage = ErrorMessage(
            errors=[{"loc": ["request"], "msg": "404 Not Found"}]
        ),
    ) -> None:
        self.code: int = 404
        self.messages: ErrorMessage = messages
        super().__init__(messages, code=self.code)


class ParsingErrorResponse(ErrorResponse):
    """Error Response for errors that happen when parsingt he request body"""

    def __init__(
        self,
    ) -> None:
        super().__init__(
            code=403,
            messages={
                "errors": [{"loc": ["body"], "msg": "Error while parsing the requst"}]
            },
        )


start_response_function = Callable[[str, list[tuple[str, str]]], Any]


class WSGIResponse:
    """
    WSGI Response Class

    It has the required properties to return a response
    """

    def __init__(
        self,
        start_response: start_response_function,
        status: str,
        headers: list[tuple[str, str]],
        body: bytes | dict[str, Any] | str,
    ) -> None:
        self.body = body
        start_response(status, headers)

    @classmethod
    def simple_response(
        cls, start_response: start_response_function, response: Response
    ):
        return WSGIResponse(
            start_response,
            status=str(response.code),
            headers=response.headers,
            body=response.body,
        )

    def send(self):
        if isinstance(self.body, bytes):
            return [self.body]
        elif isinstance(self.body, dict):
            return [bytes(json.dumps(self.body).encode("utf-8"))]

        elif isinstance(self.body, list):
            return [bytes(json.dumps(self.body).encode("utf-8"))]

        else:
            return [self.body.encode("utf-8")]


GenericResponse = Response | str | int | float | BaseModel | dict
