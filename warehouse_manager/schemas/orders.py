import datetime

from pydantic import BaseModel


class OrderItemBase(BaseModel):

    product_id: int


class OrderItemCreate(OrderItemBase):

    quantity: int


class OrderItem(OrderItemBase):

    id: int

    order_id: int

    quantity: int

    class Config:
        from_attributes = True


# order section
class OrderBase(BaseModel):
    status: str


class OrderCreate(OrderBase):

    items: list[OrderItemCreate]


class Order(OrderBase):

    id: int

    created_at: datetime

    items: list[OrderItem]

    class Config:
        from_attributes = True
