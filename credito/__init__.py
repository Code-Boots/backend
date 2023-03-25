# from server import app
import os

import pydantic
from bson import ObjectId


def run_server():
    import uvicorn

    uvicorn.run(
        "credito.server:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 9000)),
        reload=True,
    )


def run_server_prod():
    import uvicorn

    uvicorn.run(
        "credito.server:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 9000)),
        # reload=True,
    )


# This is for making the ObjectId serializable
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str  # type: ignore
