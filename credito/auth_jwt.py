from datetime import datetime, timedelta

import jwt

from credito.env import ENV
from credito.models import UserData


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 7


async def create_access_token(
    inp_data: UserData, expires_delta: timedelta | None = None
):
    data = inp_data.dict()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ENV.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_jwt(token: str):
    try:
        payload = jwt.decode(token, ENV.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise e
