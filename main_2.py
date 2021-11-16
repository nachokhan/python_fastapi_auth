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
@app.get("/items/{it_id}")
async def read_item2(it_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": it_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an item that has a long description"}
        )
    return item


# Multiple path & query params
@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int, q: Optional[str], short: bool = False):
    item = {
        "user": user_id,
        "item": item_id,
        "Q": "NO"
    }
    if q:
        item.update(
            {"Q": "SI: " + q}
        )
    if not short:
        item.update(
            {"description": "This is an item that has a long description"}
        )
    return item


# required params
@app.get("/items2/{item_id}")
async def read_user_item2(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# request body
# json info will be sent in the body of the request
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# POST no GET
@app.post("/items3/")
async def create_item(item: Item):

    new_item = {
        "The Name": item.name,
        "Anotherthing": item.price
    }

    return new_item


@app.put("/items3/{item_id}")
async def create_item2(item_id: int, item: Item, optional: Optional[str] = None):
    return {"item_id": item_id, "opt": optional, **item.dict()}


# Validations & constraints
from fastapi import Query


@app.get("/items4/")
async def read_items4(q: Optional[str] = Query(None,min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# required parameters with Query
@app.get("/items5/")
async def read_items5(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Multiple values query list
from typing import List


@app.get("/items6/")
async def read_items6(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
