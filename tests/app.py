from simpleapi import Request, Response, JSONResponse, SimpleAPI

app = SimpleAPI()


@app.get("/hello")
def hello(request: Request):
    return JSONResponse(message={"hello": "world"})


@app.post("/items")
def post_item(request: Request):
    """Returns the request body"""
    return JSONResponse(message=request.body)


app.run(port=8000)
