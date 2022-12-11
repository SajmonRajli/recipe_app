# -*- coding: utf-8 -*-
from typing import Union
from fastapi import FastAPI

app = FastAPI()

# id int PRIMARY KEY NOT NULL,
# nickname text NOT NULL,
# status bool NOT NULL,
# favorites int[],
# date_of_creation date NOT NULL,
# date_of_change date


@app.get("/")
def read_root():
    return {"Hello": "World"} 


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

	
