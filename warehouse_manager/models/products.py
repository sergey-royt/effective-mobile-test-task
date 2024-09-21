from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric

from .base import Base


class Product(Base):

    __tablename__ = "product"

    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    description: Mapped[str]

    price: Mapped[float] = mapped_column(Numeric(precision=2))

    stock_quantity: Mapped[int] = mapped_column(default=0)
