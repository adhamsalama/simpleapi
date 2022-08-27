# Dynamic Routing

A framework wouldn't be useful if it didn't support dynamic routing.

SimpleAPI supports dynamic routing using curly brackets.

An example of dynamic routing:

```python
from simpleapi import SimpleAPI, Request

app = SimpleAPI()

@app.get("/hello/{name}")
def hello_person(request: Request):
    name = request.params["name"]
    return f"Hello, {name}!"
```

Run it with `gunicorn main:app`

Open your browser at [http://localhost:8000/hello/David](http://localhost:8000/David).

You will see the response:
`Hello, David!`

If you're wondering who is David, it's [Professor David J. Mallan](https://cs.harvard.edu/malan/) of Harvard University, I owe him making me fall in love with Programming when I took his [CS50](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) course! :heart: :heart: :heart:
