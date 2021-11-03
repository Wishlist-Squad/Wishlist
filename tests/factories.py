"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist, Product
from random import randint

products = ["lamp", "shirt", "ipad", "computer mouse", "milk", "scissors", "tomato"]

class ProductFactory(factory.Factory):
    """ Creates fake Addresses """

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    # name = FuzzyChoice(choices=["lamp", "shirt", "ipad",
                    #    "computer mouse", "milk", "scissors", "tomato"])

    product_id = randint(1, len(products)+1)
    name = products[product_id-1]


class WishlistFactory(factory.Factory):
    """ Creates fake Accounts """

    class Meta:
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(
        choices=["Christmas", "Baby Timmy", "Grandaddy Jo", "Hobby", "Books"])
    customer_id = FuzzyChoice(choices=[1000, 2000])
