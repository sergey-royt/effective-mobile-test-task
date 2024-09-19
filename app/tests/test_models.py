from app.models import Base


def test_create_product(db_engine):
    Base.metadata.create_all(bind=db_engine)
