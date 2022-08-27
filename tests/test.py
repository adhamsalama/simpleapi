import json

import requests


def test_hello_world():
    response = requests.get("http://localhost:8000/hello")
    assert response.ok
    assert response.content.decode("utf-8") == "Hello, world!"


def test_global_middleware():
    response = requests.get("http://localhost:8000/global_middleware")
    assert response.ok
    assert response.content.decode("utf-8") == "True"


def test_global_and_router_middleware():
    response = requests.get("http://localhost:8000/router/router_middleware")
    assert response.ok
    assert response.json() == {"global": True, "router": True}


def test_rejecting_middleware():
    name = "adhom"
    response = requests.get(f"http://localhost:8000/unauthorized")
    assert not response.ok
    assert response.status_code == 401


def test_dynamic_routing():
    name = "adhom"
    response = requests.get(f"http://localhost:8000/greet/{name}")
    assert response.ok
    assert response.content.decode("utf-8") == f"Greetings, {name}"


def test_dynamic_route_doesnt_save_other_params():
    response = requests.get(f"http://localhost:8000/test1/ayo/test1")
    assert response.ok
    assert response.json() == {"test1": "ayo"}
    response = requests.get(f"http://localhost:8000/test1/aloha/test1")
    assert response.ok
    assert response.json() == {"test1": "aloha"}
    response = requests.get(f"http://localhost:8000/test1/oya/test2")
    assert response.ok
    assert response.json() == {"test2": "oya"}
    response = requests.get(f"http://localhost:8000/test1/ayo")
    assert response.ok
    assert response.json() == {"test1": "ayo"}
    response = requests.get(f"http://localhost:8000/test2/oya")
    assert response.ok
    assert response.json() == {"test2": "oya"}


def test_router():
    response = requests.get("http://localhost:8000/router/test")
    assert response.ok
    assert response.content.decode("utf-8") == "test"


def test_dynamic_routing_for_router():
    response = requests.get("http://localhost:8000/router/dynamic/test")
    assert response.ok
    assert response.content.decode("utf-8") == "dynamic"


def test_post_request_json():
    item = {"name": "RTX 3090", "price": "4000"}
    response = requests.post(f"http://localhost:8000/items", json=item)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == item


def test_html_response():
    response = requests.get("http://localhost:8000/html")
    assert response.ok
    assert response.headers["content-type"] == "text/html; charset=UTF-8"


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


def test_middleware():
    user = {"username": "adhom", "email": "adhom@adhom.com"}
    response = requests.post("http://localhost:8000/middleware", json=user)
    assert response.ok
    assert json.loads(response.content.decode("utf-8")) == user


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


def test_set_cookies():
    response = requests.get("http://localhost:8000/set-cookie")
    assert response.ok
    assert response.cookies.items() == [
        ("key1", "value1"),
        ("key2", "value2"),
        ("key3", "value3"),
    ]


def test_reading_cookies():
    cookies = {"name": "adhom", "age": "23"}
    response = requests.get("http://localhost:8000/set-cookie", cookies=cookies)
    assert response.ok
    assert response.json() == cookies
    # ! Test cookies whose value contain a "="
    cookies = {"jwt": "sdasdasdasd=="}
    response = requests.get("http://localhost:8000/set-cookie", cookies=cookies)
    assert response.ok
    assert response.json() == cookies


def test_set_headers():
    response = requests.get("http://localhost:8000/set-headers")
    assert response.ok
    headers = [
        ("header1", "value1"),
        ("header2", "value2"),
        ("header3", "value3"),
    ]
    for k, v in headers:
        assert k in response.headers.keys()
        assert v in response.headers.values()
        assert response.headers[k] == v


def test_reading_headers():
    headers = {"name": "adhom", "age": "23"}
    response = requests.get("http://localhost:8000/set-headers", headers=headers)
    assert response.ok
    json_response = response.json()
    for k, v in headers.items():
        assert k in json_response.keys()
        assert v in json_response.values()
        assert json_response[k] == v
