import os
from typing import Annotated, Union

import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

base_url = os.environ.get("OPENHAB_URL")


class Item(BaseModel):
    command: str


@app.post("/items/{name}")
async def send_command(name: str, item: Item, authorization: Annotated[Union[str, None], Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    headers = {
        "Authorization": authorization,
        "Accept": "application/json",
        "Content-Type": "text/plain"
    }

    result = requests.post(f"{base_url}/rest/items/{name}", headers=headers, data=item.command)

    if result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.text)
    else:
        return {}


@app.get("/items/{name}/state")
async def get_state(name: str, authorization: Annotated[Union[str, None], Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    headers = {
        "Authorization": authorization,
    }

    result = requests.get(f"{base_url}/rest/items/{name}/state", headers=headers)

    if result.status_code == 404:
        raise HTTPException(status_code=404, detail="Item not found")
    elif result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.text)
    else:
        return {'status': result.text}
