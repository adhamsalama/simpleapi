from typing import Callable, TypedDict, Any

# from request import Request
from response import Response

# ? It should take Request as a parameter but it results in circular import issue,
# ? however, APF expects a function that takes Request as a parameter so type hinting works
ViewFunction = Callable[[Any], Response]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
