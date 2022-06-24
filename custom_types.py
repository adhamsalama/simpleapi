from __future__ import annotations
from typing import Callable, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from request import Request
from response import Response

# ? It should take Request as a parameter but it results in circular import issue,
# ? however, APF expects a function that takes Request as a parameter so type hinting works
# ? Extra note: the the solution which uses TYPE_CHECKING doesn't work because in this case
# ? ViewFunction = Callable[[Request], Response] is not a type hint, but an assignment.
# ? However, I could just change Request to "Request" and it would work.
ViewFunction = Callable[["Request"], Response]


class RouteHandler(TypedDict):
    path: str
    method: str
    handler: ViewFunction
