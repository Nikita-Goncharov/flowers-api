from typing import Annotated

from fastapi import APIRouter, Header
from tortoise.exceptions import DoesNotExist

from models import init, Flower, Order, User
from api_pydantic_schemas import FlowerSchema, OrderSchema, OrderCreate, OrderCreateResponse, OrderGetResponse, FlowersGetResponse

router = APIRouter()

@router.on_event("startup")
async def on_startup():
    await init()


@router.get("/flowers", response_model=FlowersGetResponse)
async def flowers():    
    flowers = await Flower.all().values()
    return {"success": True, "data": [FlowerSchema.model_validate(f) for f in flowers], "message": ""}


@router.get("/orders", response_model=OrderGetResponse)
async def user_orders(token: Annotated[str | None, Header()]):
    orders = await Order.filter(user__token=token).values()
    # if len(orders):
    return {"success": True, "data": [OrderSchema.model_validate(f) for f in orders], "message": ""}
    # else:
    #     return {"success": False, "data": [], "message": "Error. "}


# TODO: add middleware to check token
@router.post("/orders", response_model=OrderCreateResponse)
async def create_order(order_data: OrderCreate, token: Annotated[str | None, Header()]):
    try:
        user = await User.get(token=token)
        try:
            flower = await Flower.get(name=order_data.flower_name)    
            await Order.create(
                user=user,
                flower=flower,
                quantity=order_data.quantity
            )
            return {"success": True, "message": ""}
        except DoesNotExist:
            return {"success": False, "message": "Error. There is no that flower."}
    except DoesNotExist:
            return {"success": False, "message": "Error. User not found with that creds."}

