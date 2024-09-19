import datetime
import enum
from typing_extensions import Annotated

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Numeric, func, Enum, ForeignKey, Column

from .database import Base


# mapping types

# primary key
intpk = Annotated[int, mapped_column(primary_key=True)]

# current timestamp
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


# order status choices
class OrderStatusEnum(enum.Enum):

    in_progress = "в процессе"

    sent = "отправлен"

    delivered = "доставлен"


status = Annotated[
    Enum(OrderStatusEnum),
    mapped_column(default=OrderStatusEnum.in_progress, nullable=False),
]


class Product(Base):

    __tablename__ = "product"

    id: Mapped[intpk]

    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    description: Mapped[str]

    price: Mapped[float] = mapped_column(Numeric(precision=2))

    stock_quantity: Mapped[int] = mapped_column(default=0)


class Order(Base):

    __tablename__ = "order"

    id: Mapped[intpk]

    created_at: Mapped[timestamp]

    status = Column(
        Enum(OrderStatusEnum),
        default=OrderStatusEnum.in_progress,
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):

    __tablename__ = "order_item"

    id: Mapped[intpk]

    order_id: Mapped[intpk] = mapped_column(ForeignKey("order.id"))

    product_id: Mapped[intpk] = mapped_column(ForeignKey("product.id"))

    quantity: Mapped[int]

    order: Mapped["Order"] = relationship(back_populates="items")
