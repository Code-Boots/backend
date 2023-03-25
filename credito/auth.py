from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel, Field
from starlette.config import Config
from credito.models import UserData
from fastapi.responses import RedirectResponse
from credito.types import OauthResponse
from .env import ENV
from credito.auth_jwt import create_access_token


config = Config(".env")  # read config from .env file
oauth = OAuth(
    Config(
        environ={
            "GOOGLE_CLIENT_ID": ENV.GOOGLE_CLIENT_ID,
            "GOOGLE_CLIENT_SECRET": ENV.GOOGLE_CLIENT_SECRET,
        }
    )
)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
auth_router = APIRouter()


class GoogleRedirect(BaseModel):
    url: str
    nonce: str


@auth_router.get("/login")
async def login_via_google(request: Request):
    return await oauth.google.authorize_redirect(request, ENV.REDIRECT_URL)  # type: ignore


@auth_router.get("/redirect")
async def auth_via_google(request: Request):
    """Returns a redirect Response which redirects the user to the frontend url
    it also sets the access token ( bearer Token ) in the header with key
    `x-access-token`
    """
    try:
        token = await oauth.google.authorize_access_token(request)  # type: ignore
        response = OauthResponse(**token["userinfo"])
        user = await UserData.from_db(response.email, response)
        token = await create_access_token(user)
        return RedirectResponse(
            url=f"{ENV.FRONTEND_URL}", headers={"x-access-token": token}
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"error": str(e)}
