# Example of using APF

from simpleapi import SimpleAPI, Request, Response, JSONResponse, RouteHandler
from middleware import current_user, require_validation  # type: ignore
from pydantic import BaseModel

app = SimpleAPI()


class Item(BaseModel):
    name: str
    price: float


items: list[Item] = []


@app.post("/dependency-injection")
def dep_injection(name: str, price: float):
    """View function that uses depedency injection"""
    return {"name": name, "price": price}


@app.get("/1")
def index():
    """View function that takes no parameter and returns JSONResponse"""
    return JSONResponse(message={"hello": "world"})


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


@app.get("/hello")
def hello(request: Request):
    """Returns hello world in JSON format"""
    return JSONResponse(message={"hello": "world"})


@app.get("/greet/{name}")
def greet(request: Request):
    """Dynamic route that greets users"""
    return JSONResponse(message={"greetings": request.params["name"]})


@app.get("/greet/{first_name}/{last_name}")
def greet_fullname(request: Request):
    """Multiple dynamic route that greets users"""
    fullname = request.params["first_name"] + " " + request.params["last_name"]
    return JSONResponse(message={"fullname": fullname})


@app.post("/items")
@current_user
@require_validation
def post_item(request: Request):
    """Returns the request body"""
    response = {}
    item = Item(**request.body)
    items.append(item)
    response["user"] = request.extra["user"]
    response["item"] = item.dict()
    return JSONResponse(message=response)


@app.get("/items")
def get_item(request: Request):
    q = request.query["q"][0]
    results: list[dict] = []
    for item in items:
        if q in item.name:
            results.append(item.dict())
    return JSONResponse(message=results)


@app.post("/image")
def save_image(request: Request):
    """
    Receives an image and stores it on disk.
    Assumes request content-type is multipart.
    """
    body = request.body
    try:
        image: bytes = body["image"]
        with open("image", "wb") as file:
            file.write(image)
    except Exception as e:
        print("Error while trying to save image")
        print(str(e))
        return JSONResponse(code=400, message={"message": "Invalid image"})
    # return Response(message=image, content_type="image/*") # Return the image as a response
    return JSONResponse(code=200, message={"message": "Image saved successfully"})


@app.get("/html")
def html(request: Request):
    """Returns an HTML string"""
    return Response(
        code=200,
        message="<html><body><h1>Hi</h1></body></html>",
        content_type="text/html; charset=UTF-8",
    )


@app.get("/empty")
def empty(request: Request):
    """Returns an empty response"""
    return JSONResponse()


app.run(port=8000)
