import factory

from warehouse_manager.models import Product


class UniqueFaker(factory.Faker):

    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=locale).unique


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Product

    name = UniqueFaker("word")
    description = factory.Faker("sentence", nb_words=4)
    price = factory.Faker(
        "pyfloat", positive=True, max_value=50000, right_digits=2
    )
    stock_quantity = factory.Faker("pyint", min_value=0, max_value=100)
