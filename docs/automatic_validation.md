# Automatic Validation

### A simple example

```python
from simpleapi import SimpleAPI

app = SimpleAPI()

@app.post("/create-item")
def create_item(name: str, price: int):
    return {"name": name, "price": price}
```

Here we specified that the request body will have a field called "name" and its type will be a string, and a field called "price" and its type will be an integer.

Open Postman or Insomnia (or any HTTP client you like) and send a post request to `http://localhost:8000/create-item` with the required porperties:

![dependency_injection_post](assets/dependency_injection_post.png)

### Not Sending Required Properties

So, that worked, but what happens if the request body doesn't match the arguments you specified?

Lets remove the price field from the request body and send the request again and see what will happen:

![dependency_injection_error](assets/dependency_injection_error.png)

SimpleAPI automatically validated the request body and returned an error response specifying that the request body didn't match the required arguments. In particular, the "price" field is missing.

### Sending Wrong Type of Required Fields

If you add the "price" field back, and make its value anything but an integer, SimpleAPI will return an error response specifying that the "price" field's value isn't of the required type.

An example:

![dependency_injection_error2](assets/dependency_injection_error2.png)

Note: this only supports int, float, str, and bool.
For more complex types, check and following section about Pydantic models.

### Pydantic Models

You can have more fine-grained control and specify objects using Pydantic BaseModels.

An example:

```python
from simpleapi import SimpleAPI
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    job: str
    is_alive: bool

app = SimpleAPI()

@app.post("/add-person")
def add_person(person: Person):
    person.age += 1
    return person
```

![dependency_injection_pydantic](assets/dependency_injection_pydantic.png)

If we for example removed the "is_alive" field, the automatic validation will handle it for us.

![dependency_injection_pydantic_error](assets/dependency_injection_pydantic_error.png)

### Query validation

You can also specify query parmeters.

```python
from simpleapi import Query

@app.get("/query-type-hint")
def query(
    age: Query,
    name: Query = "adhom",
):
    return JSONResponse(body={"name": name, "age": age})

```

In this example, we specified that we require a query parameter named age and another query parameter named name, which has a default value and return the queries .

If name wasn't provided by the client, then the default value will be used.

But if age wasn't provided, an error would be automatically returned.

![query_error](assets/query-error.png)

If we provide the age query, we will get this response.

![query_response](assets/query-response-1.png)

If we provide name and query, we will get this response.

![query_response](assets/query-response-2.png)

Notice that because we provied a value for name, this value was passed to the function and was used instead of the default value.

The Query type is a union of str and list[str].

If we provide multiple values for the same query parameter, it will be passed to the function as an array.
![query_response](assets/query-response-3.png)
