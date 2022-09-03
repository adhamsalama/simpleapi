# Routers

When your app gets bigger, it's a good idea to write different parts of it in separate files.

You can do this using **Routers**.

Create another file called `routers.py` and add the following code to it:

```python
from simpleapi import Router

router = Router()

@router.get("/hello")
def hello():
    return "Hello, router!"
```

And in your `main.py` file:

```python
from simpleapi import SimpleAPI
from .routers import router

app = SimpleAPI()

app.add_router(prefix="/router", router=router)
```

Open your browser at [http://localhost:8000/router/hello](http://localhost:8000/router/hello).

You will see a response that looks like this:

`Hello, router!`
