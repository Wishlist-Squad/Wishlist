"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist, Product
from random import randint


class ProductFactory(factory.Factory):
    """ Creates fake Addresses """

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["lamp", "shirt", "ipad",
                       "computer mouse", "milk", "scissors", "tomato"])


class WishlistFactory(factory.Factory):
    """ Creates fake Accounts """

    class Meta:
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(
        choices=["Christmas", "Baby Timmy", "Grandaddy Jo", "Hobby", "Books"])
    customer_id = FuzzyChoice(choices=[1000, 2000])
