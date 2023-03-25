from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr
from typing import List


PanCardType = constr(curtail_length=10, regex=r"[A-Z]{5}[0-9]{4}[A-Z]{1}")


class UserData(BaseModel):
    """User Data Model which stores personal user data"""

    name: str
    email: EmailStr
    pan: PanCardType  # type: ignore Mypy dumb


class CreditScore(BaseModel):
    """Stores the Credit Score of a User"""

    score: int
    provider: str
    latest: datetime = Field(default_factory=datetime.now)
    credit_lines: List["CreditLine"] = list()
    credit_cards: List["CreditCard"] = list()
    loans: list["Loan"] = list()


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
