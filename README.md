<div align="center">

# Warehouse manager
[![linter and tests](https://github.com/sergey-royt/effective-mobile-test-task/actions/workflows/linter-and-tests.yml/badge.svg)](https://github.com/sergey-royt/effective-mobile-test-task/actions/workflows/linter-and-tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/274b3db0d7a68f4c120f/maintainability)](https://codeclimate.com/github/sergey-royt/effective-mobile-test-task/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/274b3db0d7a68f4c120f/test_coverage)](https://codeclimate.com/github/sergey-royt/effective-mobile-test-task/test_coverage)

FastAPI powered warehouse application. A test task for [Effective mobile](https://effective-mobile.ru/#main).

<p>

<a href="#description">Description</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a>
</p>

</div>

## Description

This application dedicated to managing warehouse products and orders.

The API allows you to manage goods, inventory, and orders.

## Features:

**Products**

- Create product.
- Get list of all or specified count of products.
- Get details of certain product.
- Update product details.
- Delete product.

**Orders**

- Create order.
- Get list of all or specified count of orders.
- Get details of certain order.
- Update order status.

## Installation:

Before installing the package make sure you have Python version 3.12 or higher installed

```bash
>> python --version
Python 3.12+
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL
PostgreSQL is used as the main database management system. You have to install it first. It can be downloaded from [official website](https://www.postgresql.org/download/)

After thst you need to create database, for example using psql utility:

```sudo -u {user} psql -c 'create database {database_name};'```

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone https://github.com/sergey-royt/effective-mobile-test-task.git && cd effective-mobile-test-task
```

After that install all necessary dependencies:

```bash
>> make install
```

It's possible to not install dev dependencies if tests are not needed

```bash
>> poetry install --without dev
```

Create `.env` file in the root directory and add following variables:
```dotenv
DATABASE_URL=postgresql+psycopg2://{provider}://{user}:{password}@{host}:{port}/{database_name}
TEST_DATABASE_URL=postgresql+psycopg2://{provider}://{user}:{password}@{host}:{port}/{database_name}
POSTGRESQL_ADMIN_DATABASE_URI=postgresql+psycopg2://{provider}://{user}:{password}@{host}:{port}/{database_name}
```

or only ```DATABASE_URL``` if tests not needed

---

## Usage

Start the Uvicorn Web-server by running:

```shell
>> make start
```

By default, the server will be available at http://127.0.0.1:8000.

## Documenatation

Swagger OpenAPI documentation will be able at http://127.0.0.1:8000/docs/

### Makefile Commands

<dl>
    <dt><code>make install</code></dt>
    <dd>Install all dependencies of the package.</dd>
    <dt><code>make start</code></dt>
    <dd>Start the Uvicorn web server at http://127.0.0.1:8000</dd>
    <dt><code>make lint</code></dt>
    <dd>Check code with flake8 linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Run tests.</dd>
    <dt><code>make test-coverage</code></dt>
    <dd>Run test coverage</dd>
</dl>

### Build with
[sqlalchemy](https://www.sqlalchemy.org/) = "2.0.35"

[fastapi](https://fastapi.tiangolo.com/) = "0.115.0"

[psycopg2-binary](https://www.psycopg.org/docs/) = "2.9.9"
