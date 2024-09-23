import json
from http import HTTPStatus
from sqlalchemy import select

from warehouse_manager.models import Order, Product, OrderStatusEnum
from .conftest import client
from .factories import ProductFactory, OrderFactory, OrderItemFactory


def test_post_valid(db_session):
    stmt = select(Order)
    assert not db_session.execute(stmt).one_or_none()

    ProductFactory(stock_quantity=10)

    order_data = {"status": "", "items": [{"product_id": 1, "quantity": 5}]}

    response = client.post("/orders/", json=order_data)
    assert response.status_code == HTTPStatus.OK

    db_product = db_session.execute(
        select(Product).where(Product.id == 1)
    ).scalar()
    assert db_product.stock_quantity == 5

    stmt = select(Order).where(Order.id == 1)
    db_order = db_session.execute(stmt).scalar()
    assert db_order
    assert len(db_order.items) == 1
    assert db_order.items[0].product_id == order_data["items"][0]["product_id"]
    assert db_order.items[0].quantity == order_data["items"][0]["quantity"]
    assert len(db_session.execute(select(Order)).all()) == 1


def test_post_lack_of_product(db_session):
    stmt = select(Order)
    assert not db_session.execute(stmt).one_or_none()

    ProductFactory(stock_quantity=5)

    order_data = {"status": "", "items": [{"product_id": 1, "quantity": 10}]}

    response = client.post("/orders/", json=order_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.content == b'{"detail":"There are not enough items in stock"}'
    )
    db_product = db_session.execute(
        select(Product).where(Product.id == 1)
    ).scalar()
    assert db_product.stock_quantity == 5
    stmt = select(Order)
    assert not db_session.execute(stmt).one_or_none()


def test_read_orders_default():
    ProductFactory()
    for i in range(200):
        OrderFactory()
        OrderItemFactory(order_id=i, product_id=1, quantity=1)

    response_no_options = client.get("/orders/")
    response_list = json.loads(response_no_options.content)
    assert response_list[0]["id"] == 1
    assert len(response_list) == 100
    assert any(order["id"] < 100 for order in response_list)
    assert not any(order["id"] > 100 for order in response_list)


def test_read_orders_set_limit_anf_offset():
    ProductFactory()
    for i in range(100):
        OrderFactory()
        OrderItemFactory(order_id=i, product_id=1, quantity=1)
    response_with_options = client.get(
        "/orders/", params={"limit": 20, "skip": 35}
    )
    assert response_with_options.status_code == HTTPStatus.OK

    response_list = json.loads(response_with_options.content)
    assert response_list[0]["id"] == 36
    assert len(response_list) == 20


def test_read_order_exists():
    ProductFactory()
    ProductFactory()
    db_order1 = OrderFactory()
    db_order2 = OrderFactory()
    OrderItemFactory(order_id=1, product_id=1, quantity=1)
    OrderItemFactory(order_id=2, product_id=2, quantity=1)

    response = client.get("/orders/2/")
    assert response.status_code == HTTPStatus.OK
    response_order = json.loads(response.content)

    assert response_order["id"] == db_order2.id
    assert (
        response_order["items"][0]["product_id"]
        == db_order2.items[0].product_id
    )
    assert not response_order["created_at"] == db_order1.created_at


def test_read_order_not_exists():
    response = client.get("/orders/2/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.content == b'{"detail":"Order not found"}'


def test_patch_order_status(db_session):
    OrderFactory(status=OrderStatusEnum.processed)

    response = client.patch("/orders/1/", params={"status": "sent"})
    assert response.status_code == HTTPStatus.OK

    db_order = db_session.execute(select(Order).where(Order.id == 1)).scalar()
    assert db_order.status == OrderStatusEnum.sent


def test_patch_order_status_not_exists(db_session):
    response = client.patch("/orders/1/", params={"status": "sent"})
    assert response.status_code == HTTPStatus.NOT_FOUND
