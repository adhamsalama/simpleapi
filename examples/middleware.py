# Writing middleware is as easy as writing decorators

from simpleapi import Request, JSONResponse
from simpleapi.custom_types import ViewFunction
from functools import wraps


# def current_user(f: ViewFunction):
#     """Middleware that adds user data to the request"""
#     # ? Need wraps because normal decorator loses type hints
#     @wraps(f)
#     def decorator(request: Request):
#         print("current user middleware")
#         request.extra["user"] = {
#             "username": "adhom",
#             "email": "adhom@adhom.com",
#         }
#         return f(request)

#     return decorator


# def require_validation(f: ViewFunction):
#     """Middleware that checks user data"""
#     # ? Need wraps because normal decorator loses type hints
#     @wraps(f)
#     def decorator(request: Request):
#         print("require validation middleware")
#         user = request.extra.get("user", None)
#         if user is None:
#             return JSONResponse(code=400, body={"message": "Validation required"})
#         return f(request)

#     return decorator
