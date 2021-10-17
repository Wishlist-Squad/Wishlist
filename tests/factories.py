"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist


class WishlistFactory(factory.Factory):
    """Creates fake wishlists"""

    class Meta:
        model = Wishlist

    name = factory.Faker("name")
    customer = factory.Faker("name")
    products = factory.Faker("name")
