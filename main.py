from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


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
