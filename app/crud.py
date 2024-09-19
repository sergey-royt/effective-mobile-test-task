from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas


def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def update_product(
    db: Session, product_id: int, update_data: schemas.ProductUpdate
):
    db_product = get_product_by_id(Session, product_id)

    db_product.name = update_data.name
    db_product.description = update_data.description
    db_product.price = update_data.price
    db_product.quantity = update_data.quantity

    db_product = db.execute(
        select(models.Product).where(models.Product.id == product_id)
    ).scalar_one()

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)

    db.delete(db_product)

    db.execute(
        select(models.Product).where(models.Product.id == product_id)
    ).first()

    db.commit()


def create_order(db: Session, order: schemas.OrderCreate):

    db_order = models.Order()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    db_order.items = create_order_items(db, db_order.id, order.items)

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
    db_items = [
        models.OrderItem(order_id=order_id, **item.model_dump())
        for item in items
    ]

    db.add_all(db_items)

    db.commit()

    db.refresh(db_items)

    return db_items
