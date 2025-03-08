from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from models import User, Flower, Order


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: str = Field()
    password: str = Field()

class UserToken(BaseModel):
    token: str = Field()

class UserLoginResponse(BaseModel):
    success: bool
    token: UserToken
    message: str

class OrderCreate(BaseModel):
    flower_name: str
    quantity: int

class OrderCreateResponse(BaseModel):
    success: bool
    message: str
    
UserLogoutResponse = OrderCreateResponse

UserSchema = pydantic_model_creator(User)

class FlowerSchema(BaseModel):
    id: int
    name: str
    price: float
    type: Flower.FlowerType
    img_link: str
    

class OrderSchema(BaseModel):
    id: int
    status: Order.STATUSES
    flower: FlowerSchema
    quantity: int