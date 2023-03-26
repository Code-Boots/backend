from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

from credito.models import UserData
from .users import user_routes
from credito.auth_jwt import check_jwt
from .auth import auth_router
from .credito_brain import chat_router
from .env import ENV
from .credit_score import get_credit_score
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/docs")

security = HTTPBearer(
    bearerFormat="Bearer",
    scheme_name="Google Oauth",
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.add_middleware(SessionMiddleware, secret_key=ENV.SECRET_KEY)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_routes, prefix="/user", tags=["user"])

app.include_router(chat_router, prefix="/chat", tags=["chat"])


@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/credit_score/gen")
async def provide_credit_score(authentication: str = Header(...)):
    """Provides the latest Credit Score of a Given User"""
    try:
        data = await check_jwt(authentication)
        user_data = await UserData.from_jwt(data)
        if not user_data.is_registered:
            raise HTTPException(
                status_code=404,
                detail="User details not found. User needs to fill data to continue",
            )
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Disallowed")
    return await get_credit_score(user_data._id)
