from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr
from typing import List


class CreditLine(BaseModel):
    """Stores a credit line detail of a Credit Score"""

    latest: datetime = Field(default_factory=datetime.now)
    name: str
    provider: str
    limit: int
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

    score: int
    provider: str
    latest: datetime = Field(default_factory=datetime.now)
    credit_lines: List[CreditLine] = list()
    credit_cards: List[CreditCard] = list()
    loans: list[Loan] = list()


class OauthResponse(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: int
    exp: int


class JWTData(BaseModel):
    name: str
    uid: str
    email: str
    exp: datetime | None = None


class UserInfoData(BaseModel):
    phone: str = Field(unique=True, nullable=False)
    address1: str = Field(max_length=100, nullable=False)
    address2: str | None = Field(max_length=100, default=None)
    address3: str | None = Field(max_length=100, default=None)
    pincode: str = Field(
        max_length=7, default="1000001", nullable=False, regex=r"\d{7}"
    )

    state: str = Field(max_length=50, default="Delhi", nullable=False)

    pan: str = Field(
        max_length=10,
        min_length=10,
        nullable=False,
        unique=True,
        regex=r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    )
    dob: datetime = Field(default_factory=datetime.now, nullable=False)
