from pydantic import BaseModel
from simpleapi import JSONResponse, Request, Response, SimpleAPI
from simpleapi.response import ErrorResponse

from .routers import item


def current_user(request: Request):
    """Dummy Middleware that adds user data to the request"""
    request.extra["user"] = request.body


def global_middleware(request: Request):
    request.extra["global_middleware"] = True


def always_reject_middleware(request: Request):
    return ErrorResponse(
        code=401, messages={"errors": [{"loc": ["body"], "msg": "Not Authorized"}]}
    )


app = SimpleAPI(middleware=[global_middleware])


@app.get("/set-cookie")
def set_cookies(request: Request):
    """Sets cookies"""
    return JSONResponse(
        body=request.cookies,
        headers=[
            ("header1", "value1"),
            ("Set-Cookie", "key1=value1; Path=/"),
            ("Set-Cookie", "key2=value2; Path=/"),
            ("Set-Cookie", "key3=value3;"),
        ],
    )


@app.get("/set-headers")
def set_headers(request: Request):
    """Sets headers"""
    return JSONResponse(
        body=request.headers,
        headers=[("header1", "value1"), ("header2", "value2"), ("header3", "value3")],
    )


@app.get("/test1/{test1}")
def aa(request: Request):
    return request.params


@app.get("/test2/{test2}")
def ba(request: Request):
    return request.params


@app.get("/test1/{test1}/test1")
def a(request: Request):
    return request.params


@app.get("/test1/{test2}/test2")
def b(request: Request):
    return request.params


@app.get("/unauthorized", middleware=[always_reject_middleware])
def reject():
    return "This shouldn't be returned"


app.add_router(prefix="/router", router=item.router)


class Item(BaseModel):
    name: str
    price: float


items: list[Item] = []


@app.get("/hello")
def hello(request: Request):
    """Test hello world"""
    return "Hello, world!"


@app.get("/global_middleware")
def global_middleware_router(request: Request):
    return request.extra["global_middleware"]


@app.get("/greet/{name}")
def greet(request: Request):
    """Test dynamic routing"""
    return f"Greetings, {request.params['name']}"


@app.post("/items")
def post_item(request: Request):
    """Test post request returning body as JSON"""
    return JSONResponse(body=request.body)


@app.get("/400")
def status_400():
    return Response(code=400, body="", content_type="string")


@app.put("/put")
def put(request: Request):
    return JSONResponse(body=request.body)


@app.patch("/patch")
def patch(request: Request):
    return JSONResponse(body=request.body)


@app.delete("/delete")
def delete():
    return ""


@app.head("/head")
def head():
    return ""


@app.options("/options")
def options():
    return ""


@app.post("/middleware", middleware=[current_user])
def middleware(request: Request):
    """Tests middleware"""
    return JSONResponse(body=request.extra["user"])


@app.get("/query")
def query(request: Request):
    """Test request parameters"""
    return JSONResponse(body=request.query)


@app.post("/dependency-injection")
def dependency_injection(name: str, price: float):
    """Test dependency injection"""
    return {"name": name, "price": price}


@app.post("/dependency-injection-error")
def dependency_injection_error(name: str, price: float, active: bool):
    """Test dependency injection"""
    # ? SimpleAPI should automatically return an error with this ever executing
    return {"name": name, "price": price}


@app.post("/dependency-injection")
def dep_injection(name: str, price: float):
    """View function that uses depedency injection"""
    return {"name": name, "price": price}


@app.get("/1")
def index():
    """View function that takes no parameter and returns JSONResponse"""
    return JSONResponse(body={"hello": "world"})


@app.get("/2")
def index2():
    """View function that takes no parameter and returns a string"""
    return "Hello, World!"


@app.get("/3")
def index3():
    """View function that takes no parameter and returns an int"""
    return 12


@app.get("/4")
def index4():
    """View function that takes no parameter and returns a float"""
    return 20.56


@app.get("/5")
def index5():
    """View function that takes no parameter and returns a dict"""
    person = {"name": "adhom", "age": 23}
    return person


@app.get("/6")
def index6():
    """View function that takes no parameter and returns a Pydantic BaseModel"""
    item = Item(name="some item", price=2000)
    return item


@app.get("/greet/{first_name}/{last_name}")
def greet_fullname(request: Request):
    """Multiple dynamic route that greets users"""
    fullname = request.params["first_name"] + " " + request.params["last_name"]
    return JSONResponse(body={"fullname": fullname})


@app.post("/pydantic-item")
def post_pydantic_item(item: Item):
    return item


@app.get("/items")
def get_item(request: Request):
    q = request.query["q"][0]
    results: list[dict] = []
    for item in items:
        if q in item.name:
            results.append(item.dict())
    return JSONResponse(body=results)


@app.post("/image")
def save_image(request: Request):
    """
    Receives an image and stores it on disk.
    Assumes request content-type is multipart.
    """
    try:
        image: bytes = request.form["image"]
        with open("image", "wb") as file:
            file.write(image)
    except Exception as e:
        print("Error while trying to save image")
        print(str(e))
        return JSONResponse(code=400, body={"body": "Invalid image"})
    return Response(
        body=image, content_type="image/*"
    )  # Return the image as a response


@app.get("/html")
def html():
    """Returns an HTML string"""
    return Response(
        code=200,
        body="<html><body><h1>Hi</h1></body></html>",
        content_type="text/html; charset=UTF-8",
    )


@app.get("/empty")
def empty():
    """Returns an empty response"""
    return ""
