from sqlalchemy.orm import Session


class ProductRepository:
    def get_products(self, db: Session, skip: int = 0, limit: int = 100):
        pass
