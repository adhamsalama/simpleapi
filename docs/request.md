# Request

The Request object contains severl useful properties.

Properties:

-   environ (The WSGI environ).
-   method (The request HTTP method)
-   path (The request path).
-   params (The route's dynamic parameters).
-   form (The request body's form data).
-   body (The request's JSON body).
-   query (The request's query parameters).
-   headers (The request's headers).
-   cookies (The requests's cookies).
-   extra (A dict to which middleware can add fields).

Source Code: [https://github.com/adhamsalama/simpleapi/blob/main/simpleapi/request.py](https://github.com/adhamsalama/simpleapi/blob/main/simpleapi/request.py)
