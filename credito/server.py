from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from .users import user_routes
from credito.auth_jwt import check_jwt
from .auth import auth_router
from .env import ENV
from .credit_score import get_credit_score
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import HTTPBearer

app = FastAPI(docs_url="/docs")

security = HTTPBearer(
    bearerFormat="Bearer",
    scheme_name="Google Oauth",
)

app.add_middleware(SessionMiddleware, secret_key=ENV.SECRET_KEY)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_routes, prefix="/user", tags=["user"])


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
