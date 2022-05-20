# Example of using APF

from apf import APF, Request, Response, JSONResponse

app = APF()


@app.get("/hello")
def hello(request: Request):
    return JSONResponse(message={"hello": "world"})


@app.get("/hi")
def hi(request: Request):
    return Response(
        code=200,
        message="<html><body><h1>Hello</h1></body></html>",
        content_type="text/html; charset=UTF-8",
    )


app.run("localhost", 8080, multithreading=True)
