# First Steps

This tutorial shows you how to use SimpleAPI with most of its features, step by step.

You can copy the code blocks to a file named `main.py` and run it with `gunicorn main:app`.

The simplest SimpleAPI file looks like this:

Create a file `main.py` with:

```python

from simpleapi import SimpleAPI

app = SimpleAPI()

@app.get("/hello")
def hello():
    return "Hello, world!"
```

Run it with `gunicorn main:app`

Open your browser at [http://localhost:8000/hello](http://localhost:8000/hello).

You will see the response:
`Hello, world!`

You can also specify other HTTP methods, for example:

```python
@app.post("/hello")
def hello_post():
    return "Hello, world!"

@app.put("/hello")
def hello_put():
    return "Hello, world!"

@app.patch("/hello")
def hello_patch():
    return "Hello, world!"

@app.delete("/hello")
def hello_delete():
    return "Hello, world!"
```

**Notice** that if your function doesn't need the request object, you can just not specify it as a parameter.
