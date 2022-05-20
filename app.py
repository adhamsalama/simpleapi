# Example of using APF

from apf import APF, Request

app = APF()


@app.get("/hello")
def hello(request: Request):
    request.json_response(200, {"hello": "world"})


app.run("localhost", 8080, multithreading=True)
