from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with given name already existed"
        )
    return crud.create_product(db, product)


@app.get("/products/", response_model=list[schemas.Product])
def read_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}/", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/products/{product_id}/", response_model=schemas.Product)
def update_product(
    product_id: int,
    update_data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    db_product = crud.update_product(db, product_id, update_data)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}/")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product successfully deleted"}


@app.post("/orders/", response_model=schemas.OrderCreate)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order)
    if not db_order:
        raise HTTPException(
            status_code=400, detail="There are not enough items in stock"
        )
    return db_order


@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}/", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.patch("/orders/{order_id}/", response_model=schemas.Order)
def update_order_status(
    order_id: int, status: str, db: Session = Depends(get_db)
):
    db_order = crud.update_order_status(db, order_id, status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
