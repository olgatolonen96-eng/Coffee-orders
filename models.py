import enum
from typing import Optional
from pydantic import BaseModel, Field
#enum
class UserRole(str, enum.Enum):
    customer = "customer"
    barista = "barista"
    admin = "admin"


class OrderStatus(str, enum.Enum):
    created = "created"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"


class DrinkSize(str, enum.Enum):
    small = "S"
    medium = "M"
    large = "L"
#Menu
class Drink(BaseModel):
        name: str
        base_price: float = Field(gt=0)
        available_sizes: list[DrinkSize] = [DrinkSize.small, DrinkSize.medium, DrinkSize.large]

class AddOn(BaseModel):
        name: str
        price: float = Field(ge=0)

#Bin

class CartItem(BaseModel):
    drink_id: int
    size: DrinkSize
    add_on_ids: list[int] = []
    quantity: int = Field(gt=0, default=1)
#Order
class Order(BaseModel):
    id: Optional[int] = None
    user_id: int
    items: list[dict]
    status: OrderStatus = OrderStatus.created
    total_price: float
#Users
class UserRegister(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole



