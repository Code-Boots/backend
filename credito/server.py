from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from credito.auth_jwt import check_jwt
from .auth import auth_router
from credito.models import UserData
from .env import ENV
from .credit_score import get_credit_score
from .types import CreditScore
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import HTTPBearer

app = FastAPI(docs_url="/docs")

security = HTTPBearer(
    bearerFormat="Bearer",
    scheme_name="Google Oauth",
)

app.add_middleware(SessionMiddleware, secret_key=ENV.SECRET_KEY)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/credit_score/gen")
async def provide_credit_score(authentication: str = Header(...)):
    """Provides the latest Credit Score of a Given User"""
    try:
        await check_jwt(authentication)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Disallowed")
    return get_credit_score()


# @app.post("/credit_score")
# async def create_credit_score(credit_score: CreditScore):
#     """Creates a Credit Score for a Given User"""

#     return credit_score


# @app.post("/user/create")
# async def create_user(user_data: UserData):
#     return await user_data.create_one()
