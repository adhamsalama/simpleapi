# Example of using APF

from apf import APF, Request, Response, JSONResponse
from middleware import current_user, require_validation

app = APF()


@app.get("/hello")
def hello(request: Request):
    """Returns hello world in JSON format"""
    return JSONResponse(message={"hello": "world"})


@app.post("/items")
@current_user
@require_validation
def post_item(request: Request):
    """Returns the request body"""
    body = request.body
    body["user"] = request.extra["user"]
    return JSONResponse(message=body)


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
