from os import getenv

from pydantic import BaseModel, Field


class ENVWrapper(BaseModel):
    DATABASE_URL: str = Field(default=getenv("DATABASE_URL"))
    MONGODB_URL: str = Field(default=getenv("MONGODB_URL"))
    SECRET_KEY: str = Field(default=getenv("SECRET_KEY"))
    GOOGLE_CLIENT_ID: str = Field(default=getenv("GOOGLE_CLIENT_ID"))
    GOOGLE_CLIENT_SECRET: str = Field(default=getenv("GOOGLE_CLIENT_SECRET"))
    FRONTEND_URL: str = Field(default=getenv("FRONTEND_URL", "http://localhost:3000"))
    REDIRECT_URL: str = Field(
        default=getenv("REDIRECT_URL", "http://localhost:8000/auth/redirect")
    )


ENV = ENVWrapper()
