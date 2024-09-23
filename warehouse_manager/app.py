from fastapi import FastAPI


tags_metadata = [
    {"name": "products", "description": "Operations with products."},
    {"name": "orders", "description": "Operations with orders."},
]

description = """
The API allows you to manage goods, inventory, and orders.

## Products

You can:

* **Create** product.
* **Get list** of all or specified count of products.
* **Get details** of certain product.
* **Update** product details.
* **Delete** product.

## Orders

You can:

* **Create** order.
* **Get list** of all or specified count of orders.
* **Get details** of certain order.
* **Update** order status.
"""
app = FastAPI(
    title="Warehouse manager API",
    summary="FastAPI application for managing warehouse "
    "products and orders, with Auto docs for the API.",
    description=description,
    contact={
        "name": "Sergey Roytberg",
        "email": "sergeiroitberg@yandex.ru",
    },
    openapi_tags=tags_metadata,
)
