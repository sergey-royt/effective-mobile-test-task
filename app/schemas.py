from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str

    description: str

    price: float

    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(BaseModel):

    id: int

    class Config:
        from_attributes = True


# order item section
class OrderItemBase(BaseModel):

    product_id: int


class OrderItemCreate(OrderItemBase):

    order_id: int

    quantity: int


class OrderItem(OrderItemBase):

    id: int

    order_id: int

    quantity: int

    class Config:
        from_attributes = True


# order section
class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):

    status: str

    items: list[OrderItem]


class Order(OrderBase):

    id: int

    created_at: datetime

    status: str

    items: list[OrderItem]

    class Config:
        from_attributes = True
