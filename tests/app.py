from simpleapi import Request, Response, JSONResponse, SimpleAPI, response, custom_types

app = SimpleAPI()


from simpleapi import Request, JSONResponse


def current_user(f: custom_types.ViewFunction):
    """Middleware that adds user data to the request"""

    def decorator(request: Request):
        request.extra["user"] = request.body
        return f(request)

    return decorator


@app.get("/hello")
def hello():
    """Test hello world"""
    return "Hello, world!"


@app.get("/greet/{name}")
def greet(request: Request):
    """Test dynamic routing"""
    return f"Greetings, {request.params['name']}"


@app.post("/items")
def post_item(request: Request):
    """Test post request returning body as JSON"""
    return JSONResponse(message=request.body)


@app.get("/html")
def html():
    """Test returning an HTML string"""
    return Response(
        code=200,
        message="<html><body><h1>Hi</h1></body></html>",
        content_type="text/html",
    )


@app.get("/400")
def status_400():
    return Response(code=400, message="", content_type="string")


@app.put("/put")
def put(request: Request):
    return JSONResponse(message=request.body)


@app.patch("/patch")
def patch(request: Request):
    return JSONResponse(message=request.body)


@app.delete("/delete")
def delete():
    return ""


@app.head("/head")
def head():
    return ""


@app.options("/options")
def options():
    return ""


@app.post("/middleware")
@current_user
def middleware(request: Request):
    """Tests middleware"""
    return JSONResponse(message=request.extra["user"])


@app.get("/query")
def query(request: Request):
    """Test request parameters"""
    return JSONResponse(message=request.query)


@app.post("/dependency-injection")
def dependency_injection(name: str, price: float):
    """Test dependency injection"""
    return {"name": name, "price": price}


@app.post("/dependency-injection-error")
def dependency_injection_error(name: str, price: float, active: bool):
    """Test dependency injection"""
    # ? SimpleAPI should automatically return an error with this ever executing
    return {"name": name, "price": price}


app.run(port=8000)
