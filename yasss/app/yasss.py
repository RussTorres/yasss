import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import yasss_json

ENVIRON_ROOT_PATH = os.getenv("YASSS_ROOT_PATH")
yasss_app = FastAPI(root_path=ENVIRON_ROOT_PATH)

yasss_app.include_router(yasss_json.router)

# FIXME do something here
origins = ["*"]

yasss_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)