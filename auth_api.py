from typing import Annotated

import bcrypt
from fastapi import APIRouter, Header
from tortoise.exceptions import DoesNotExist, IntegrityError

from models import User
from api_pydantic_schemas import UserRegister, UserLogin, UserLoginResponse, UserSchema, UserLogoutResponse, UserRegisterResponse

router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
async def register(user: UserRegister):
    try:    
        # Hash the password before saving
        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

        # Create the user in the database
        user_obj = await User.create(
            username=user.username,
            email=user.email,
            password_hash=hashed_password,  # Save hashed password
            is_active=True,
        )
        return {"success": True, "data": await UserSchema.from_tortoise_orm(user_obj), "message": ""}
    except IntegrityError:
        return {"success": False, "data": {}, "message": "Error. User already exists with that creds."}


@router.post("/login", response_model=UserLoginResponse)
async def login(user_creds: UserLogin):
    try:
        user = await User.get(email=user_creds.email)
        if bcrypt.checkpw(user_creds.password.encode("utf-8"), user.password_hash.encode()) and user.token == "":
            print("here")
            user.token = bcrypt.gensalt().decode("utf-8")
            await user.save()
            return {"success": True, "token": user.token, "message": ""}
        else:
            return {"success": False, "token": "", "message": "Error. User not found with that creds."}
    except DoesNotExist:
        return {"success": False, "token": "", "message": "Error. User not found with that creds."}


@router.post("/logout", response_model=UserLogoutResponse)
async def logout(token: Annotated[str | None, Header()]):
    try:
        user = await User.get(token=token)
        user.token = ""
        await user.save()
        return {"success": True, "message": ""}
    except DoesNotExist:
        return {"success": False, "message": "Error. User not found with that token."}
