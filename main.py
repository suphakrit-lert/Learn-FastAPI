from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


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
