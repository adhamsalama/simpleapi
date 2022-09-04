# Middleware

SimpleAPI offers fine-grained control over middleware.

There are 3 types of middleware:

1. Global middleware.
1. Router middleware.
1. Function middleware.

### Global Middleware

Global middleware is applied globally on all route handlers.

It's defined as a normal function that takes a request as a parameter.

Example:

```python
from simpleapi import SimpleAPI, Request

def global_middleware(request: Request):
    """Logger middleware"""
    print(f"Path: {request.path}")

app = SimpleAPI(middleware=[global_middleware])

@app.get("/hello")
def hello():
    return "Hello, world!"
```

If you check the terminal, you will see this:
`Path: /hello`

You can add as many middleware as you want to the middleware array. They will be executed in order.

### Router Middleware

Router middleware is applied to all of the router's route handlers.

Example:

```python
from simpleapi import Router, Request

def router_middleware(request: Request):
    """Logger middleware"""
    print(f"Path: {request.path}"

router = Router(middleware=[router_middleware])

@router.get("/hello")
def hello():
    return "Hello, router!"
```

This will print the path of all router handlers under this specific router, it won't execute for any other route handlers that aren't under this specific router.

### Function Middleware

Function middleware is applied to its specific function only.

Example:

```python
from simpleapi import SimpleAPI, Request

def function_middleware(request: Request):
    """Logger middleware"""
    print("This is the /hello route")

app = SimpleAPI()

@app.get("/hello", middleware=[function_middleware])
def hello():
    return "Hello, world!"
```
