from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World2"}


# Order matters

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Predefined Values
from enum import Enum


class ParamOptions(str, Enum):
    juan_name = "juan"
    maria = "maria"
    pepe = "pepe"


@app.get("/names/{name}")
def get_name(name: ParamOptions):

    text_to_show = "It's Pepe"
    if name == ParamOptions.juan_name:
        text_to_show = "It's Juan"
    elif name == ParamOptions.maria.value:
        text_to_show = "It's Maria"

    return {
        "Option": name,
        "Nombre": text_to_show
    }


# Path Values
@app.get("/files/{file_path:path}/{item}")
async def read_file(file_path: str, item: int):
    return {
        "file_path": file_path, "item": item
    }


# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


# Opcional Parameters
@app.get("/items/{item_id}")
def get_item_id(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": f"SI:{q}"}
    return {"item_id": item_id, "q": "NO"}
