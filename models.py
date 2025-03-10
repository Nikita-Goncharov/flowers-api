from enum import Enum

from tortoise import Tortoise, fields, models


class User(models.Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    token = fields.CharField(max_length=128, default="")
    
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    
    class PydanticMeta:
        exclude = ["password_hash"]
        
    def __str__(self):
        return f"{self.username} - {self.email}"


class Flower(models.Model):
    class FlowerType(str, Enum):
        red = "red"
        yellow = "yellow"
        pink = "pink"
        white = "white"
        azure = "azure"
        blue = "blue"
        orange = "orange"
        purple = "purple"
    
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=20, unique=True)
    price = fields.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    type = fields.CharEnumField(enum_type=FlowerType, max_length=20, default=FlowerType.white)
    img_link = fields.CharField(default="", max_length=500) # TODO: img with img local save
    
    def __str__(self):
        return f"{self.name}({self.type}) - {self.price}"


class Order(models.Model):
    class STATUSES(Enum):
        pending = "pending"
        completed = "completed"
        failed = "failed"
    
    id = fields.IntField(primary_key=True)
    status = fields.CharEnumField(STATUSES, max_length=20, default=STATUSES.pending)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    flower = fields.ForeignKeyField("models.Flower", related_name="orders")
    quantity = fields.IntField(default=1)

    def __str__(self):
        return f"{self.user} - order_id: {self.id}"

config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': 'db',
                'port': 5432,
                'user': 'postgres',
                'password': 'password',
                'database': 'flower_store',
                'minsize': 1,
                'maxsize': 1000,
            }
        }
    },
    'apps': {
        'models': {
            'models': [ 'models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}

async def init():
    await Tortoise.init(
        config=config
    )
    # await Tortoise.generate_schemas()
