from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
import json
from fastapi.testclient import TestClient

from warehouse_manager.models import Product
from .factories import ProductFactory


def test_post_valid(db_session: Session, client: TestClient):
    stmt = select(Product)
    assert not db_session.execute(stmt).one_or_none()

    product_data = {
        "name": "sofa",
        "description": "some sofa",
        "price": 1500,
        "stock_quantity": 10,
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == HTTPStatus.OK
    stmt = select(Product).where(Product.name == product_data["name"])
    db_product = db_session.execute(stmt).scalar()
    assert db_product
    assert db_product.name == product_data["name"]
    assert db_product.description == product_data["description"]
    assert db_product.price == product_data["price"]
    assert db_product.stock_quantity == product_data["stock_quantity"]
    assert len(db_session.execute(select(Product)).all()) == 1


def test_post_missing_name(db_session: Session, client: TestClient):
    stmt = select(Product)
    assert not db_session.execute(stmt).one_or_none()

    missing_name_data = {
        "description": "some sofa",
        "price": 1500,
        "stock_quantity": 10,
    }

    response = client.post("/products/", json=missing_name_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert not db_session.execute(stmt).one_or_none()

    expected_content = (
        b'{"detail":[{'
        b'"type":"missing",'
        b'"loc":["body","name"],'
        b'"msg":"Field required",'
        b'"input":'
        b'{"description":"some sofa",'
        b'"price":1500,'
        b'"stock_quantity":10}}]}'
    )

    assert expected_content == response.content


def test_post_existed(db_session: Session, client: TestClient):
    stmt = select(Product)
    assert not db_session.execute(stmt).one_or_none()

    product_data = {
        "name": "sofa",
        "description": "some sofa",
        "price": 1500,
        "stock_quantity": 10,
    }

    db_product = Product(**product_data)
    db_session.add(db_product)
    db_session.commit()
    assert len(db_session.execute(select(Product)).all()) == 1

    response = client.post("/products/", json=product_data)
    assert (
        response.content == b'{"detail":'
        b'"Product with given name already existed"}'
    )
    assert len(db_session.execute(select(Product)).all()) == 1


def test_read_products_default(db_session: Session, client: TestClient):
    for i in range(200):
        ProductFactory()

    response_no_options = client.get("/products/")
    response_list = json.loads(response_no_options.content)
    assert len(response_list) == 100


def test_read_products_set_limit(db_session: Session, client: TestClient):
    for i in range(60):
        ProductFactory()
    response_with_options = client.get("/products/", params={"limit": 20})
    response_list = json.loads(response_with_options.content)
    assert len(response_list) == 20


def test_read_product_exists(db_session: Session, client: TestClient):
    db_product1 = ProductFactory()
    db_product2 = ProductFactory()

    response = client.get(f"/products/{db_product2.id}")
    response_product = json.loads(response.content)

    assert response_product["id"] == db_product2.id
    assert response_product["name"] == db_product2.name
    assert not response_product["description"] == db_product1.description


def test_read_not_exists(client: TestClient):
    response = client.get("products/1")
    assert response.content == b'{"detail":"Product not found"}'


def test_update_exists(db_session: Session, client: TestClient):
    db_product = ProductFactory(name="sofa")

    update_data = {
        "name": "chair",
        "description": "some chair",
        "price": 780.5,
        "stock_quantity": 100,
    }

    response = client.put(f"/products/{db_product.id}", json=update_data)
    assert response.status_code == HTTPStatus.OK

    stmt = select(Product).where(Product.id == db_product.id)
    db_product = db_session.execute(stmt).scalar()

    assert db_product.name == update_data["name"]
    assert db_product.description == update_data["description"]
    assert db_product.price == update_data["price"]
    assert db_product.stock_quantity == update_data["stock_quantity"]


def test_update_not_exists(client: TestClient):
    update_data = {
        "name": "chair",
        "description": "some chair",
        "price": 780.5,
        "stock_quantity": 100,
    }

    response = client.put("/products/1", json=update_data)
    assert response.content == b'{"detail":"Product not found"}'


def test_delete(db_session: Session, client: TestClient):
    db_product = ProductFactory()

    response = client.delete(f"/products/{db_product.id}")

    assert response.status_code == HTTPStatus.OK

    stmt = select(Product).where(Product.id == db_product.id)
    assert not db_session.execute(stmt).one_or_none()
