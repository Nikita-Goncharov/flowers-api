from fastapi import APIRouter
from tortoise.exceptions import DoesNotExist

from models import init, Flower, Order, User
from api_pydantic_schemas import UserToken, FlowerSchema, OrderSchema, OrderCreate, OrderCreateResponse

router = APIRouter()

@router.on_event("startup")
async def on_startup():
    await init()


@router.get("/flowers", response_model=list[FlowerSchema])
async def flowers():    
    flowers = await Flower.all()
    return [FlowerSchema.model_validate(f) for f in flowers]


@router.get("/orders", response_model=list[OrderSchema])
async def user_orders(user_creds: UserToken):
    flowers = await Order.filter(user__token=user_creds.token)
    return [OrderSchema.model_validate(f) for f in flowers]


# TODO: add middleware to check token
@router.post("/orders", response_model=OrderCreateResponse)
async def create_order(user_creds: UserToken, order_data: OrderCreate):
    user = await User.get(token=user_creds.token)
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

