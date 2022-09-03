# SimpleAPI

![banner](https://i.imgur.com/Q3kFiKf.png)
SimpleAPI is a minimalistic, unopinionated web framework for Python, inspired by FastAPI & Flask.

SimpleAPI is a WSGI compliant framework.

This is a hobby project made for educational purposes because I want to try learning writing a web server framework.

So, this is obviously not meant for production environments.

Development of SimpleAPI is tracked at [this](https://github.com/users/adhamsalama/projects/1) GitHub project.

## Installation

`pip install simplestapi`

## Usage

An example of using SimpleAPI:

Copy the following code to a file called `app.py`

```python
from simpleapi import SimpleAPI

app = SimpleAPI()

@app.get("/hello")
def hello():
    return "Hello, world!"
```

Run it with `gunicorn app:app`

More examples can be found in [tests](./tests)

## Documentation

[https://adhamsalama.github.io/simpleapi](https://adhamsalama.github.io/simpleapi)

---

![django_kofta](./docs/assets/django_kofta.png)
