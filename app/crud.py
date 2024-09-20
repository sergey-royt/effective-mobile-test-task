from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas


def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(models.Product).offset(skip).limit(limit)

    return db.execute(stmt).scalars()


def get_product_by_id(db: Session, product_id: int):
    stmt = select(models.Product).where(models.Product.id == product_id)

    result = db.execute(statement=stmt).scalar()

    return result


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_product_quantity(db: Session, product_id: int):
    stmt = select(models.Product.stock_quantity).where(models.Product.id == product_id)
    return db.execute(stmt).scalar_one_or_none()


def reduce_product_quantity(db: Session, product_id: int, r_value: int):
    db_product = get_product_by_id(db, product_id)

    db_product.quantity -= r_value

    stmt = select(models.Product).where(models.Product.id == product_id)

    db_product = db.execute(stmt).scalar_one()

    db.commit()

    db.refresh(db_product)

    return db_product


def update_product(
    db: Session, product_id: int, update_data: schemas.ProductUpdate
):
    db_product = get_product_by_id(db, product_id)

    db_product.name = update_data.name
    db_product.description = update_data.description
    db_product.price = update_data.price
    db_product.stock_quantity = update_data.stock_quantity

    db_product = db.execute(
        select(models.Product).where(models.Product.id == product_id)
    ).scalar()

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)

        db.execute(
            select(models.Product).where(models.Product.id == product_id)
        ).first()

        db.commit()

        return True



def create_order(db: Session, order: schemas.OrderCreate):

    db_order = models.Order()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    db_order.items = create_order_items(db, db_order.id, order.items)
    if not db_order.items:
        db.delete(db_order)
        db.execute(
            select(models.Order).where(models.Order.id == db_order.id)
        ).first()
        db.commit()
        return None

    db_order = db.execute(
        select(models.Order).where(models.Order.id == db_order.id)
    ).scalar_one()
    db.commit()
    db.refresh(db_order)

    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def change_order_status(db: Session, order_id: int, status: str):
    db_order = get_order_by_id(db, order_id)

    db_order.status = status

    db_order = db.execute(
        select(models.Product).where(models.Product.id == order_id)
    ).scalar_one()

    db.commit()
    db.refresh(db_order)

    return db_order


def create_order_items(
    db: Session, order_id: int, items: list[schemas.OrderItem]
):
    db_items = []

    for item in items:
        if item.quantity > get_product_quantity(db, item.id):
            return None

        reduce_product_quantity(db, item.product_id, item.quantity)

        db_items.append(
            models.OrderItem(order_id=order_id, **item.model_dump())
        )

    db.add_all(db_items)

    db.commit()

    db.refresh(db_items)

    return db_items
