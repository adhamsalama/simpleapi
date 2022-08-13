# PYTHONPATH=.. python test.py

from subprocess import Popen, PIPE
import json


def test_hello_world():
    # Run the server
    process1 = Popen(["python", "app.py"], stdout=PIPE, stderr=PIPE)
    process = Popen(["http", "localhost:8000/hello"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process1.kill()
    assert stdout.decode("utf-8") == '{"hello": "world"}'


def test_post_request():
    # Run the server
    process1 = Popen(["python", "app.py"], stdout=PIPE, stderr=PIPE)
    process = Popen(
        ["http", "localhost:8000/items?q=anything", "name=RTX4090", "price=9000"],
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = process.communicate()
    body = json.loads(stdout.decode("utf-8"))
    process1.kill()
    assert body == {"name": "RTX4090", "price": "9000"}


test_hello_world()

test_post_request()
