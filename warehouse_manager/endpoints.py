from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .app import app

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """
    Generate database session
    :return: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product, tags=["products"])
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    """
    Create product with given credentials.

    **request body:**
    - **name** (str, unique),
    - **description** (str),
    - **price** (int | number),
    - **stock_quantity** (int)

    **return:** Created product, or raise 400 http exception if product with given name
    already exists.
    """

    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with given name already existed"
        )
    return crud.create_product(db, product)


@app.get("/products/", response_model=list[schemas.Product], tags=["products"])
def read_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve list of products with given params.

    **params:**
    - **skip:** (int) n products to skip from beginning. default=0
    - **limit:** (int) max quantity of products to be shown. default=100

    **return** By default list of first 100 products, you can manage this
    behaviour specifying 'skip' and 'limit' params.
    """

    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get(
    "/products/{product_id}/",
    response_model=schemas.Product,
    tags=["products"],
)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve product details.

    **params:**
    - **product_id:** (int) product id

    **return:** The details of product by given id, or raise 404 http exception
    if product with given id doesn't exist.
    """

    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put(
    "/products/{product_id}/",
    response_model=schemas.Product,
    tags=["products"],
)
def update_product(
    product_id: int,
    update_data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    Update product with given data.

    **params:**
    - **product_id:** product id (int)

    **request body:**
    - **name** (str, unique),
    - **description** (str),
    - **price** (int | number),
    - **stock_quantity** (int)

    **return:** Updated product or raise 404 http exception
    if product with given id not found.
    """

    db_product = crud.update_product(db, product_id, update_data)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}/", tags=["products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product with given id.

    **params:**
    - **product_id:** product id (int)

    **return:** Success message or raise 404 http exception if product not found.
    """

    if not crud.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product successfully deleted"}


@app.post("/orders/", response_model=schemas.OrderCreate, tags=["orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create order with given credentials.

    **request body:**
    - **status:** status (str),
    - **items:** items [
                {product_id (int),
                quantity (int)}
                ]

    **return:** Created order or raise 400 http exception
    if order items are empty or if it's not enough of products in stock.
    """
    if not order.items:
        raise HTTPException(
            status_code=400, detail="Order should contain at least one item"
        )
    db_order = crud.create_order(db, order)
    if not db_order:
        raise HTTPException(
            status_code=400, detail="There are not enough items in stock"
        )
    return db_order


@app.get("/orders/", response_model=list[schemas.Order], tags=["orders"])
def read_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve list of orders with given params.

    **params:**
    - **skip:** (int) n orders to skip from beginning. default=0
    - **limit:** (int) max orders of products to be shown. default=100

    **return** By default list of first 100 orders, you can manage this
    behaviour specifying 'skip' and 'limit' params.
    """

    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}/", response_model=schemas.Order, tags=["orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve order details.

    **params:**
    - **product_id:** (int) order id

    **return:** The details of order by given id, or raise 404 http exception
    if order with given id doesn't exist.
    """
    db_order = crud.get_order_by_id(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.patch(
    "/orders/{order_id}/", response_model=schemas.Order, tags=["orders"]
)
def update_order_status(
    order_id: int, status: str, db: Session = Depends(get_db)
):
    """
    Update order status.

    **params:**

    - **order_id:** order id (int)
    - **status:** new order status (str)

    **return:** order with updated status or raise 404 http exception
    if order not found.
    """
    db_order = crud.update_order_status(db, order_id, status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
