import json
import requests


def test_hello_world():
    response = requests.get("http://localhost:8000/hello")
    assert response.ok
    assert response.content.decode("utf-8") == "Hello, world!"


def test_dynamic_routing():
    name = "adhom"
    response = requests.get(f"http://localhost:8000/greeting/{name}")
    assert response.ok
    assert response.content.decode("utf-8") == f"Greetings, {name}"


def test_post_request_json():
    item = {"name": "RTX 3090", "price": "4000"}
    response = requests.post(f"http://localhost:8000/items", json=item)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == item


def test_html_response():
    response = requests.get("http://localhost:8000/html")
    assert response.ok
    assert response.headers["content-type"] == "text/html"


def test_status_code_400():
    response = requests.get("http://localhost:8000/400")
    assert response.status_code == 400


def test_put_request():
    item = {"hello": "world"}
    response = requests.put("http://localhost:8000/put", json=item)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == item


def test_patch_request():
    item = {"hello": "world"}
    response = requests.patch("http://localhost:8000/patch", json=item)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == item


def test_delete_request():
    response = requests.delete("http://localhost:8000/delete")
    assert response.ok


def test_head_request():
    response = requests.head("http://localhost:8000/head")
    assert response.ok


def test_options_request():
    response = requests.options("http://localhost:8000/options")
    assert response.ok


# def test_middleware():
#     user = {"username": "adhom", "email": "adhom@adhom.com"}
#     response = requests.post("http://localhost:8000/middleware", json=user)
#     assert response.ok
#     assert json.loads(response.content.decode("utf-8")) == user


def test_get_query_request():
    response = requests.get(f"http://localhost:8000/query?q=cats&p=dogs")
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == {
        "q": "cats",
        "p": "dogs",
    }


def test_dependency_injection():
    item = {"name": "RTX 3090", "price": 3000.50}
    response = requests.post("http://localhost:8000/dependency-injection", json=item)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == item


def test_dependency_injection_error():
    item = {"name": "RTX 3090", "price": 3000.50}
    response = requests.post(
        "http://localhost:8000/dependency-injection-error", json=item
    )
    assert not response.ok
    assert response.status_code == 403
    assert response.json() == {
        "errors": [
            {
                "loc": ["active"],
                "msg": "Property active is required to be of type bool but it's missing",
            }
        ]
    }


def test_router_get():
    response = requests.get("http://localhost:8000/router/test")
    assert response.ok
    assert response.text == "test"


def test_router_post():
    response = requests.post("http://localhost:8000/router/test")
    assert response.ok
    assert response.text == "test"


def test_not_found():
    response = requests.get("http://localhost:8000/non-exisiting-route")
    assert not response.ok
    assert response.status_code == 404
    assert response.json() == {"errors": [{"loc": ["request"], "msg": "404 Not Found"}]}
