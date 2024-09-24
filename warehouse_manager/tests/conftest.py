from typing import Generator
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import ProgrammingError
import os
from fastapi.testclient import TestClient

from warehouse_manager.app import app
from warehouse_manager.database import Base
from warehouse_manager.endpoints import get_db
from warehouse_manager.tests.factories import (
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
)


TEST_DB_URL: str = os.getenv("TEST_DATABASE_URL")
POSTGRESQL_ADMIN_DATABASE_URI: str = os.getenv("POSTGRESQL_ADMIN_DATABASE_URI")

admin_engine = create_engine(
    POSTGRESQL_ADMIN_DATABASE_URI, isolation_level="AUTOCOMMIT"
)
engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def create_test_database():
    """Create the test database if it doesn't exist."""
    with admin_engine.connect() as connection:
        try:
            connection.execute(
                text(f"CREATE DATABASE {TEST_DB_URL.split('/')[-1]}")
            )
        except ProgrammingError:
            print("Database already exists, continuing...")


@pytest.fixture(scope="function")
def db_session():
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    connection = engine.connect()
    transaction = connection.begin()
    session_ = TestingSessionLocal(bind=connection)

    yield session_

    session_.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    create_test_database()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def set_session_for_factories(db_session: Session):

    ProductFactory._meta.sqlalchemy_session = db_session
    OrderFactory._meta.sqlalchemy_session = db_session
    OrderItemFactory._meta.sqlalchemy_session = db_session


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
