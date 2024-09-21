from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from typing_extensions import Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    """
    Base model with primary key field.
    Every other database model inherits from it
    """

    id: Mapped[intpk]
