from datetime import datetime, timedelta

import jwt

from credito.env import ENV
from credito.models import UserData
from credito.types import JWTData


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 7


async def create_access_token(
    inp_data: UserData, expires_delta: timedelta | None = None
):
    to_encode = JWTData(
        name=inp_data.name,
        uid=str(inp_data.uid),
        email=inp_data.email,
    )
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    encoded_jwt = jwt.encode(
        to_encode.dict(include={"exp": expire}), ENV.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def check_jwt(token: str):
    try:
        payload = jwt.decode(token, ENV.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise e
