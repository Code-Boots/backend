from fastapi import APIRouter, HTTPException, Header
from chatbot.chat import chatbot

from credito.auth_jwt import check_jwt
from .env import ENV
from pydantic import BaseModel

CreditoChat = chatbot(ENV.CREDITO_API_KEY)
chat_router = APIRouter()


class Message(BaseModel):
    credit_score: int
    num_cards: int
    question: str


@chat_router.post("/message")
async def post_message(message: Message, authentication: str = Header(...)):
    """Posts a message to the chatbot"""
    try:
        await check_jwt(authentication)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Disallowed")
    return CreditoChat.getAns(message.credit_score, message.num_cards, message.question)
