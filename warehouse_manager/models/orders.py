import enum
import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing_extensions import Annotated
from sqlalchemy import Enum, func, Column, ForeignKey

from .base import Base


class OrderStatusEnum(enum.Enum):

    processed = "в обработке"

    in_progress = "в процессе"

    sent = "отправлен"

    delivered = "доставлен"


timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


status = Annotated[
    Enum(OrderStatusEnum),
    mapped_column(default=OrderStatusEnum.in_progress, nullable=False),
]


class Order(Base):

    __tablename__ = "order"

    created_at: Mapped[timestamp]

    status = Column(
        Enum(OrderStatusEnum),
        default=OrderStatusEnum.processed,
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):

    __tablename__ = "order_item"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    quantity: Mapped[int]

    order: Mapped["Order"] = relationship(back_populates="items")
