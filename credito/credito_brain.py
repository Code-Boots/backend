from typing import Dict, List
from fastapi import APIRouter, HTTPException, Header
from chatbot.chat import chatbot

from credito.auth_jwt import check_jwt
from .env import ENV
from pydantic import BaseModel

MAX_CHAT_COUNT = 5

CreditoChat = chatbot(ENV.CREDITO_API_KEY)
chat_router = APIRouter()


CreditoChatMemory: Dict[str, List[Dict]] = {}


class Message(BaseModel):
    credit_score: int
    num_cards: int
    question: str


@chat_router.post("/message")
async def post_message(message: Message, authentication: str = Header(...)):
    """Posts a message to the chatbot"""
    try:
        resp = await check_jwt(authentication)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Disallowed")

    brain = CreditoChatMemory.get(resp.uid, list())

    CreditoChat.questionBank = brain  # type: ignore

    answer = CreditoChat.getAns(
        message.credit_score, message.num_cards, message.question
    )
    if len(brain) > MAX_CHAT_COUNT:
        brain = brain[1:]
    CreditoChatMemory[resp.uid] = CreditoChat.questionBank  # type: ignore
    return answer
