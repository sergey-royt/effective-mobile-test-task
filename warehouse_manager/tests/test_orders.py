import json
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from .factories import ProductFactory, OrderFactory, OrderItemFactory

from warehouse_manager.models import Order, Product, OrderStatusEnum


def test_post_valid(db_session: Session, client: TestClient):
    stmt = select(Order)
    assert not db_session.execute(stmt).one_or_none()

    db_product = ProductFactory(stock_quantity=10)

    order_data = {
        "status": "",
        "items": [{"product_id": db_product.id, "quantity": 5}],
    }

    response = client.post("/orders/", json=order_data)
    assert response.status_code == HTTPStatus.OK

    db_product = db_session.execute(
        select(Product).where(Product.id == db_product.id)
    ).scalar()
    assert db_product.stock_quantity == 5

    stmt = select(Order)
    db_order = db_session.execute(stmt).scalar_one_or_none()
    assert db_order
    assert len(db_order.items) == 1
    assert db_order.items[0].product_id == order_data["items"][0]["product_id"]
    assert db_order.items[0].quantity == order_data["items"][0]["quantity"]
    assert len(db_session.execute(select(Order)).all()) == 1


def test_read_orders_default(client: TestClient):
    db_product = ProductFactory()
    for i in range(200):
        order = OrderFactory()
        OrderItemFactory(
            order_id=order.id, product_id=db_product.id, quantity=1
        )

    response_no_options = client.get("/orders/")
    response_list = json.loads(response_no_options.content)
    assert len(response_list) == 100


def test_read_orders_set_limit(client: TestClient):
    product = ProductFactory()
    for i in range(100):
        order = OrderFactory()
        OrderItemFactory(order_id=order.id, product_id=product.id, quantity=1)
    response_with_options = client.get("/orders/", params={"limit": 20})
    assert response_with_options.status_code == HTTPStatus.OK

    response_list = json.loads(response_with_options.content)
    assert len(response_list) == 20


def test_read_order_exists(client: TestClient):
    product1 = ProductFactory()
    product2 = ProductFactory()
    order1 = OrderFactory()
    order2 = OrderFactory()
    OrderItemFactory(order_id=order1.id, product_id=product1.id, quantity=1)
    OrderItemFactory(order_id=order2.id, product_id=product2.id, quantity=1)

    response = client.get(f"/orders/{order2.id}/")
    assert response.status_code == HTTPStatus.OK
    response_order = json.loads(response.content)

    assert response_order["id"] == order2.id
    assert (
        response_order["items"][0]["product_id"] == order2.items[0].product_id
    )
    assert not response_order["created_at"] == order1.created_at


def test_read_order_not_exists(client: TestClient):
    response = client.get("/orders/2/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.content == b'{"detail":"Order not found"}'


def test_patch_order_status(db_session: Session, client: TestClient):
    order = OrderFactory(status=OrderStatusEnum.processed)

    response = client.patch(f"/orders/{order.id}/", params={"status": "sent"})
    assert response.status_code == HTTPStatus.OK

    db_order = db_session.execute(
        select(Order).where(Order.id == order.id)
    ).scalar()
    assert db_order.status == OrderStatusEnum.sent


def test_patch_order_status_not_exists(
    db_session: Session, client: TestClient
):
    response = client.patch("/orders/1/", params={"status": "sent"})
    assert response.status_code == HTTPStatus.NOT_FOUND
