from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select, ScalarResult

from . import models, schemas


# products section
def create_product(
    db: Session, product: schemas.ProductCreate
) -> schemas.Product:
    """
    :param db: session object
    :param product: product containing at least name, description, price,
    and stock quantity
    :return: created product
    """

    db_product = models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(
    db: Session, skip: int = 0, limit: int = 100
) -> ScalarResult[Any]:
    """
    :param db: session object
    :param skip: count of products to skip (from beginning)
    :param limit: max count of products to be shown
    :return: scalar result with retrieved products
    """

    stmt = select(models.Product).offset(skip).limit(limit)
    return db.execute(stmt).scalars()


def get_product_by_id(db: Session, product_id: int) -> schemas.Product | None:
    """
    :param db: session object
    :param product_id: product id
    :return: product with given id or None if there's no match
    """

    stmt = select(models.Product).where(models.Product.id == product_id)
    result = db.execute(statement=stmt).scalar()
    return result


def get_product_by_name(db: Session, name: str) -> schemas.Product | None:
    """
    :param db: session object
    :param name: product name
    :return: product with given name or None if there's no match
    """

    stmt = select(models.Product).where(models.Product.name == name)
    result = db.execute(statement=stmt).scalar()
    return result


def get_product_quantity(db: Session, product_id: int) -> int | None:
    """
    :param db: session object
    :param product_id: product id
    :return: stock quantity of product with given id
    or None if product not found
    """

    stmt = select(models.Product.stock_quantity).where(
        models.Product.id == product_id
    )
    return db.execute(stmt).scalar_one_or_none()


def reduce_product_quantity(
    db: Session, product_id: int, r_value: int
) -> schemas.Product | None:
    """
    :param db: session object
    :param product_id: product id
    :param r_value:
    :return: product if stock quantity reducing passed successfully
    or None if there is not enough products in stock
    """

    if r_value > get_product_quantity(db, product_id):
        return None

    db_product = get_product_by_id(db, product_id)
    db_product.stock_quantity -= r_value

    stmt = select(models.Product).where(models.Product.id == product_id)

    db.execute(stmt).scalar_one()

    db.commit()

    db.refresh(db_product)

    return db_product


def update_product(
    db: Session, product_id: int, update_data: schemas.ProductUpdate
) -> schemas.Product | None:
    """
    :param db: session object
    :param product_id: product id
    :param update_data: new product data including fields:
    name, description, price, stock_quantity
    :return: updated product
    """

    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
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


def delete_product(db: Session, product_id: int) -> None:
    """
    :param db: session object
    :param product_id: product id
    :return: delete product with given id if presented
    """

    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)

        db.execute(
            select(models.Product).where(models.Product.id == product_id)
        ).first()

        db.commit()


# orders section
def create_order(
    db: Session, order: schemas.OrderCreate
) -> schemas.Order | None:
    """
    :param db: session object
    :param order: order containing order items
    :return: created order or None if there is not enough products
    """

    db_order = models.Order()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    create_order_items(db, db_order.id, order.items)
    db.refresh(db_order)

    if not db_order.items:
        db.delete(db_order)
        db.execute(
            select(models.Order).where(models.Order.id == db_order.id)
        ).first()
        db.commit()
        return None

    return db_order


def get_orders(
    db: Session, skip: int = 0, limit: int = 100
) -> ScalarResult[Any]:
    """
    :param db: session object
    :param skip: count of orders to skip (from beginning)
    :param limit: max count of orders to be shown
    :return: scalar result with retrieved orders
    """

    stmt = select(models.Order).offset(skip).limit(limit)
    return db.execute(stmt).scalars()


def get_order_by_id(db: Session, order_id: int) -> schemas.Order | None:
    """
    :param db: session object
    :param order_id: order id
    :return: order with given id or None if there's no match
    """

    stmt = select(models.Product).where(models.Order.id == order_id)
    result = db.execute(statement=stmt).scalar()
    return result


def update_order_status(
    db: Session, order_id: int, status: str
) -> schemas.Order:
    """
    :param db: session object
    :param order_id: order id
    :param status: new order status
    :return: updated order
    """
    db_order = get_order_by_id(db, order_id)

    db_order.status = status

    db_order = db.execute(
        select(models.Order).where(models.Order.id == order_id)
    ).scalar_one()

    db.commit()
    db.refresh(db_order)

    return db_order


def create_order_items(
    db: Session, order_id: int, items: list[schemas.OrderItemCreate]
) -> list[schemas.OrderItemCreate] | None:
    """
    :param db: session object
    :param order_id: order id
    :param items: order items
    :return: return list of created order items
    or None if they weren't created cause of lack in stock
    """
    db_items = []
    for item in items:
        if not reduce_product_quantity(db, item.product_id, item.quantity):
            db.rollback()
            return None

        db_item = models.OrderItem(
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db_items.append(db_item)

    db.add_all(db_items)

    db.commit()

    return db_items
