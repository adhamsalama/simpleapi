import json
from typing import Any, get_type_hints

from pydantic import BaseModel, ValidationError

from .custom_types import RouteHandler
from .request import Request
from .response import JSONResponse, Response


def handle_request(request: Request, handlers: list[RouteHandler]) -> Response:
    """
    A method that tries to find the matching route handler.
    """

    for handler in handlers:
        # ? Check dynamic routes
        is_dynamic = False
        if "{" in handler["path"] and "}" in handler["path"]:  # ['/greet/{name}']
            # ? Ignore first slash
            # ! This wont work for trailing backslash
            handler_path = handler["path"].split("/")[
                1:
            ]  # path = ['greet', '{name}']
            request_path = request.path.split("/")[1:]
            if len(handler_path) == len(request_path):
                is_dynamic = True
                for handler_part, request_part in zip(handler_path, request_path):
                    if (
                        handler_part[0] == "{" and handler_part[-1] == "}"
                    ):  # handler_part = '{name}'
                        request.params[handler_part[1:-1]] = request_part

        if handler["method"] == request.method and (
            handler["path"] == request.path or is_dynamic
        ):
            handler_type_hints = get_type_hints(handler["handler"])
            dependency_injection: dict[str, Any] = {}
            for k, v in handler_type_hints.items():
                if v == Request:
                    dependency_injection[k] = request
                elif k in request.body.keys():
                    if isinstance(request.body[k], v):
                        dependency_injection[k] = request.body[k]
                    elif type(v) == type(BaseModel):
                        try:
                            dependency_injection[k] = v.parse_obj(request.body[k])
                        except ValidationError as e:
                            return Response(code=403, body={"error": {"fields": k, "info": e.errors()}}, content_type="application/json")
                    else:
                        return Response(code=403, body={"error": {"fields": k, "info": f"Property {k} is required to be of type {v.__name__}"}}, content_type="application/json")
                else:
                    return Response(code=403, body=f"Error: Property {k} is required to be of type {v.__name__} but it's missing", content_type="string")
            if handler_type_hints and not dependency_injection:
                return Response(code=403, body={"errors": {"fields": handler_type_hints.keys(), "types": [t.__name__ for t in handler_type_hints.values()]}}, content_type="string")
                
            response = handler["handler"](**dependency_injection)
            if isinstance(response, str):
                constructed_response = Response(
                    code=200, body=response, content_type="string"
                )
            elif isinstance(response, (int, float)):
                constructed_response = Response(
                    code=200, body=str(response), content_type="string"
                )
            elif isinstance(response, JSONResponse):
                constructed_response = response
            elif isinstance(response, Response):
                constructed_response = response
            elif isinstance(response, BaseModel):
                # Pydantic BaseModel
                constructed_response = Response(
                    code=200,
                    body=response.json(),
                    content_type="application/json",
                )
            elif isinstance(response, dict):
                # Dict
                constructed_response = Response(
                    code=200,
                    body=json.dumps(response),
                    content_type="application/json",
                )
            else:
                raise Exception("Unsupported Return Type from View Function")
            return constructed_response
    return Response(code=404, body="404", content_type="string")
