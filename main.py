import random
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator, BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return ({"user_id": "the current user"},)


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "you are using alexnet"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    Input file name

    **Example:**
    http://127.0.0.1:8000/files//home/johndoe/myfile.txt
    """
    return {"file_path": file_path}

    # @app.get("/items/")
    # async def read_item(skip: int = 0, limit: int = 10):
    #     """
    #     Query version
    #     http://127.0.0.1:8000/items/
    #     http://127.0.0.1:8000/items/?skip=0&limit=10
    #     """
    #     return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    """
    >>> http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
    {"item_id":"foo-item","needy":"sooooneedy","skip":0,"limit":null}
    """
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    """
    http://127.0.0.1:8000/items/foo?short=True
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    """
    >>> curl -X 'PUT' \
    'http://127.0.0.1:8000/items/1?q=axs' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
    }'
    
    {
    "item_id": 1,
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0,
    "q": "axs"
    }
    """
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


## Chapter 4. Query Param & Validation
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern=r"\w{2}\d{2}",
        ),
    ] = None,
):
    """
    Annotated can be used to add metadata to your parameters

    For a default value,
    >>> async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items2/")
async def read_items2(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    """
    >>> http://localhost:8000/items2/
    >>> http://localhost:8000/items2/?q=foo&q=bar
    {"q":["foo","bar"]}
    """
    query_items = {"q": q}
    return query_items


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


@app.get("/items3/")
async def read_items3(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
