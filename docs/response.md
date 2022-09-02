# Responses

You can return strings, dicts, integers, floats, Pydantic models right in your view function and SimpleAPI will automatically handle returning them as HTTP responses.

But what if you want more control?

## Response

The Base Response class contains severl useful properties and methods.
All response classes inherit this class.

Properties:

-   code (The response status code, default = 200)
-   body (The response body)
-   headers (The response headers).
-   content_type (The response content-type, default = text/html; charset=UTF-8)

Methods:

-   set_header (Sets a response header).
-   set_cookie (Sets a response cookie).

## JSONResponse

The JSON Response class inherits everything from the Response class, except it sets the response content-type to application/json by default.

## Example

To return a response with a 404 status code and a body of "Can't find this resource", and the content-type as text/html:

```python
from simpleapi import SimpleAPI, Response

app = SimpleAPI()

@app.get("/not-found")
def not_found():
    response = Response(
        code=404,
        body="Can't Find this resource",
        content_type="text/html; charset=UTF-8"
    )
    return response
```
