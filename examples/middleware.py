# Writing middleware is as easy as writing decorators

from simpleapi import Request, JSONResponse
from simpleapi.custom_types import ViewFunction


def current_user(f: ViewFunction):
    """Middleware that adds user data to the request"""

    def decorator(request: Request):
        print("current user middleware")
        request.extra["user"] = {
            "username": "adhom",
            "email": "adhom@adhom.com",
        }
        return f(request)

    return decorator


def require_validation(f: ViewFunction):
    """Middleware that checks user data"""

    def decorator(request: Request):
        print("require validation middleware")
        user = request.extra.get("user", None)
        if user is None:
            return JSONResponse(code=400, message={"message": "Validation required"})
        return f(request)

    return decorator
