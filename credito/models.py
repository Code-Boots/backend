from datetime import datetime
from typing import List, cast
from bson import ObjectId
from pydantic import EmailStr, constr

from credito.database import PyObjectId
from credito.types import JWTData, OauthResponse, UserInfoData
from .env import ENV
from pydantic import BaseModel, Field
from .database import db

AddressType = constr(max_length=100)


class UserData(BaseModel):
    """User Data Model which stores personal user data"""

    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", exclude=True)
    name: str = Field(...)
    avatar: str | None = Field(...)
    email: EmailStr = Field(unique=True, nullable=False)
    phone: str | None = Field(default=None, max_length=10, unique=True, nullable=True)
    address1: str | None = Field(max_length=100, default=None)
    address2: str | None = Field(max_length=100, default=None)
    address3: str | None = Field(max_length=100, default=None)
    pincode: str | None = Field(default=None, max_length=7)
    state: str | None = Field(default=None, max_length=50)

    pan: str | None = Field(  # type: ignore Mypy dumb
        default=None,
        min_length=10,
        max_length=10,
        unique=True,
        nullable=True,
        regex=r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    )
    dob: datetime = Field(default_factory=datetime.now, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    is_registered: bool = Field(default=False)

    @property
    def uid(self) -> str:
        return str(self._id)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    async def create_one(self) -> "UserData":
        """Creates a USER Data"""
        res = await db["user_data"].insert_one(self.dict())
        return self

    @staticmethod
    async def from_oauth_response(response: OauthResponse) -> "UserData":
        return UserData(
            name=response.name,
            email=cast(EmailStr, response.email),
            avatar=response.picture,
        )

    @staticmethod
    async def from_db(email: str, oauth_data: OauthResponse) -> "UserData":
        """Updates data if user exists else creates a new user"""
        data: UserData | None = await db["user_data"].find_one({"email": email})
        data = UserData(**data) if isinstance(data, dict) else None  # type: ignore
        if not data:
            data = await UserData.from_oauth_response(response=oauth_data)
            await data.create_one()
            return data
        return data

    @staticmethod
    async def from_jwt(token: JWTData) -> "UserData":
        data: UserData | None = await db["user_data"].find_one({"id": token.uid})
        data = UserData(**data) if isinstance(data, dict) else None
        if not data:
            raise ValueError("User not found")
        return data

    async def update_registration(self, regis_data: UserInfoData):
        """Updates the user registration data"""
        await db["user_data"].update_one(
            {"_id": self._id}, {"$set": regis_data.dict(exclude={"email"})}
        )
        return self


class CreditLine(BaseModel):
    """Stores a credit line detail of a Credit Score"""

    latest: datetime = Field(default_factory=datetime.now)
    name: str = Field(...)
    provider: str = Field(...)
    limit: int = Field(...)
    overdue: bool = False
    next_due_date: datetime = Field(default_factory=datetime.now)
    left_to_pay: int


class CreditCard(BaseModel):
    """Stores a credit card detail of a Credit Score"""

    latest: datetime = Field(default_factory=datetime.now)
    name: str
    bank_name: str
    limit: int
    used: int
    overdue: bool = False
    next_due_date: datetime = Field(default_factory=datetime.now)


class Loan(BaseModel):
    """Stores a loan detail of a Credit Score"""

    latest: datetime = Field(default_factory=datetime.now)
    type: str
    provider: str
    total: int
    overdue: bool = False
    next_due_date: datetime = Field(default_factory=datetime.now)
    left_to_pay: int
    tenure: int


class CreditScore(BaseModel):
    """Stores the Credit Score of a User"""

    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int = Field(foreign_key="user_data.id")
    score: int
    provider: str
    latest: datetime = Field(default_factory=datetime.now)
    credit_lines: List[CreditLine] = list()
    credit_cards: List[CreditCard] = list()
    loans: list[Loan] = list()
