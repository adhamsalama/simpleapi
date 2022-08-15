# SimpleAPI

SimpleAPI is a minimalistic, unopinionated web framework for Python, inspired by FastAPI & Flask.

This is a hobby project made for educational purposes because I want to try learning writing a web server framework.

So, this is obviously not meant for production environments.

Development of SimpleAPI is tracked at [this](https://github.com/users/adhamsalama/projects/1) GitHub project.

How to install:

`pip install simplestapi`

An example of using SimpleAPI:

```python
from simpleapi import SimpleAPI

app = SimpleAPI()

@app.get("/hello")
def hello():
    """Returns hello world as a string"""
    return "Hello, world!"

app.run(port=8000)

```

More examples can be found in /examples
