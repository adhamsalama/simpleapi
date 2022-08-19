# Examples of fucntions as middleware
from simpleapi import Request


def current_user(request: Request):
    """Middleware that adds user data to the request"""
    request.extra["user"] = {
        "username": "adhom",
        "email": "adhom@adhom.com",
    }
