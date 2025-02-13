from fastapi import APIRouter, HTTPException
from controllers.token_controller import TokenController
from models.token_model import Token_user, Token


router = APIRouter()

nuevo_token = TokenController()



@router.post("/generate_token")
async def generate_token(user: Token_user):
    rpta = nuevo_token.generate_token(user)
    return rpta

@router.post("/verify_token")
async def verify_token(token: Token):
    rpta = nuevo_token.verify_token(token)
    return rpta