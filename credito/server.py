from fastapi import FastAPI
from pydantic import BaseModel
from .credit_score import get_credit_score
from .types import CreditScore, UserData

# from .credit_score import get_credit_score

app = FastAPI(docs_url="/docs")


@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/gen/credit_score")
def provide_credit_score(user_data: UserData):
    """Provides the latest Credit Score of a Given User"""
    return get_credit_score(user_data)
