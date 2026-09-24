from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
