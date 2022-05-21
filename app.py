# Example of using APF

from apf import APF, Request, Response, JSONResponse

app = APF()


@app.get("/hello")
def hello(request: Request):
    """Returns hello world in JSON format"""
    return JSONResponse(message={"hello": "world"})


@app.post("/items")
def post_item(request: Request):
    """Returns the request body"""
    body = request.body
    return JSONResponse(message=body)


@app.post("/image")
def save_image(request: Request):
    """Receives an image and stores it on disk"""
    body = request.body
    try:
        image: bytes = body["image"]
        with open("image", "wb") as file:
            file.write(image)
    except Exception as e:
        print("Error while trying to save image")
        print(str(e))
        return JSONResponse(code=400, message={"message": "Invalid image"})
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


app.run("localhost", 8080, multithreading=True)
