from fastapi import APIRouter
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from middlewares.jwt_bearer import admin_email, admin_password
from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == admin_email and user.password == admin_password:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)