import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from warehouse_manager.database import Base
from warehouse_manager.main import app, get_db
from warehouse_manager.tests.factories import ProductFactory

# should encapsulate
DB_URL = os.getenv("TEST_DATABASE_URL")


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",
        action="store",
        default=DB_URL,
        help="url of the database to use for tests",
    )


@pytest.fixture(scope="session")
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = request.config.getoption("--dburl")
    engine_ = create_engine(db_url, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    ProductFactory._meta.sqlalchemy_session = session_

    session_.begin()
    yield session_

    session_.rollback()


@pytest.fixture(scope="function", autouse=True)
def test_db(db_engine):
    Base.metadata.create_all(bind=db_engine)
    yield
    Base.metadata.drop_all(bind=db_engine)


@pytest.fixture(scope="function", autouse=True)
def session_override(db_session):
    def get_db_override():
        try:
            db = db_session
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_override
