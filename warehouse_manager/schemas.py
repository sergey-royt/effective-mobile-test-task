from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str

    description: str = Field(description="description of the product")

    price: float = Field(
        gt=0, description="The price must be greater than zero"
    )

    stock_quantity: int = Field(
        default=0, description="Quantity of product in stock"
    )


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

    quantity: int = Field(gt=0, description="Can't be less than 1")

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
