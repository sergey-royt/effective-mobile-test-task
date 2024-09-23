from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str

    description: str

    price: float

    stock_quantity: int | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):

    id: int

    model_config = ConfigDict(from_attributes=True)


# order item section
class OrderItemBase(BaseModel):

    product_id: int


class OrderItemCreate(OrderItemBase):

    quantity: int


class OrderItem(OrderItemBase):

    id: int

    order_id: int

    quantity: int

    model_config = ConfigDict(from_attributes=True)


# order section
class OrderBase(BaseModel):
    status: str


class OrderCreate(OrderBase):

    items: list[OrderItemCreate]


class Order(OrderBase):

    id: int

    created_at: datetime

    items: list[OrderItem]

    model_config = ConfigDict(from_attributes=True)
