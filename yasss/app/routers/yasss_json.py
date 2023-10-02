import json
import os
import posixpath
import uuid

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import (RedirectResponse, JSONResponse)


root_storage_path = os.environ.get("YASSS_STORAGE_PATH", "/yasss_storage")
server_path = os.environ.get("YASSS_SERVER_PATH")

router = APIRouter()


def idx_to_path(idx):
    # 256 files/directories max per level
    idxpath = os.path.join(
        *[idx[i:i+2] for i in range(0, 32, 2)])
    return os.path.join(root_storage_path, idxpath)
    

def get_idx_contents(idx):
    idxpath = idx_to_path(idx)
    with open(idxpath, "rb") as f:
        contents = f.read()
    return contents


def save_to_idx(contents):
    uu = uuid.uuid4().hex
    idxpath = idx_to_path(uu)
    # TODO paranoid try/except
    os.makedirs(os.path.dirname(idxpath), exist_ok=True)
    with open(idxpath, "wb") as f:
        f.write(contents)
    return uu


@router.post("/json", response_class=JSONResponse, status_code=201)
async def post_json(input_j=Body(...)):
    input_json = jsonable_encoder(input_j)
    idx = save_to_idx(json.dumps(input_json).encode())
    return posixpath.join(server_path, "json", idx)


@router.get("/json/{idx}", response_class=JSONResponse, status_code=200)
async def get_json(idx):
    return json.loads(get_idx_contents(idx))

