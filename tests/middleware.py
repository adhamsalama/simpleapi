# Examples of fucntions as middleware
from simpleapi import Request


def current_user(request: Request):
    """Middleware that adds user data to the request"""
    request.extra["user"] = {
        "username": "adhom",
        "email": "adhom@adhom.com",
    }


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
