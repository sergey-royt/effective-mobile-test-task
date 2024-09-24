import factory

from warehouse_manager.models import Product, Order, OrderItem


class UniqueFaker(factory.Faker):

    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=locale).unique


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Product
        sqlalchemy_session_persistence = "commit"

    name = UniqueFaker("word")
    description = factory.Faker("sentence", nb_words=4)
    price = factory.Faker(
        "pyfloat", positive=True, max_value=50000, right_digits=2
    )
    stock_quantity = factory.Faker("pyint", min_value=0, max_value=100)


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "commit"


class OrderItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderItem
        sqlalchemy_session_persistence = "commit"
