from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DECIMAL, Integer


class Base(DeclarativeBase):
    pass


class Product(Base):

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(30))

    description: Mapped[str] = mapped_column(String)

    price: Mapped[float] = mapped_column(DECIMAL(precision=2))

    stock_quantity: Mapped[int] = mapped_column(Integer)
