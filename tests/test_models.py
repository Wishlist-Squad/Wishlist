"""
This code is adapted from Prof. Rofrano 's Pet model test code
"""

"""
Test cases for Wishlist Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_models.py:TestWishlistModel
"""

import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Wishlist, DataValidationError, db, Product
from service import app
from .factories import WishlistFactory, ProductFactory
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  Wishlist   M O D E L   T E S T   C A S E S
######################################################################


class TestWishlist(unittest.TestCase):
    """ Test Cases for Wishlist Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    def _create_wishlist(self, products=[]):
        """ Creates an wishlist from a Factory """
        fake_wishlist = WishlistFactory()
        wishlist = Wishlist(
            name=fake_wishlist.customer_id,
            customer_id=fake_wishlist.customer_id,
            products=products
        )
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        return wishlist

    def _create_product(self):
        """ Creates fake products from factory """
        fake_product = ProductFactory()
        product = Product(
            name=fake_product.name,
        )
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        return product

######################################################################
#  T E S T   C A S E S
######################################################################

    def test_create_an_wishlist(self):
        """ Create a Wishlist and assert that it exists """
        fake_wishlist = WishlistFactory()
        wishlist = Wishlist(
            name=fake_wishlist.name,
            customer_id=fake_wishlist.customer_id,
        )
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, fake_wishlist.name)
        self.assertEqual(wishlist.customer_id, fake_wishlist.customer_id)

    def test_add_a_wishlist(self):
        """ Create an wishlist and add it to the database """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = self._create_wishlist()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_update_wishlist(self):
        """ Update an wishlist """
        wishlist = self._create_wishlist()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)

        # Fetch it back
        wishlist = Wishlist.find_by_customer_and_id(
            wishlist.customer_id, wishlist.id)
        wishlist.name = "Random Stuff"
        wishlist.save()

        # Fetch it back again
        wishlist = Wishlist.find_by_customer_and_id(
            wishlist.customer_id, wishlist.id)
        self.assertEqual(wishlist.name, "Random Stuff")

    def test_delete_an_wishlist(self):
        """ Delete an wishlist from the database """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = self._create_wishlist()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 0)

    def test_find_or_404(self):
        """ Find or throw 404 error """
        wishlist = self._create_wishlist()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)

        # Fetch it back
        wishlist = Wishlist.find_or_404(wishlist.id)
        self.assertEqual(wishlist.id, 1)

    def test_find_by_name(self):
        """ Find by name """
        wishlist = self._create_wishlist()
        wishlist.create()

        # Fetch it back by name
        same_wishlist = Wishlist.find_by_name(wishlist.name)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.name, wishlist.name)

    def test_find_by_customer(self):
        wishlist = self._create_wishlist()
        wishlist.create()

        same_wishlist = Wishlist.find_by_customer(wishlist.customer_id)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.name, wishlist.name)

    def test_serialize_a_wishlist(self):
        """ Serialize an wishlist """
        product = self._create_product()
        wishlist = self._create_wishlist(products=[product])
        serial_wishlist = wishlist.serialize()
        self.assertEqual(serial_wishlist['id'], wishlist.id)
        self.assertEqual(serial_wishlist['name'], wishlist.name)
        self.assertEqual(serial_wishlist['customer_id'], wishlist.customer_id)
        self.assertEqual(len(serial_wishlist['products']), 1)
        products = serial_wishlist['products']
        self.assertEqual(products[0]['id'], product.id)
        self.assertEqual(products[0]['name'], product.name)
        self.assertEqual(products[0]['wishlist_id'], product.wishlist_id)

    def test_deserialize_an_wishlist(self):
        """ Deserialize an wishlist """
        product = self._create_product()
        wishlist = self._create_wishlist(products=[product])
        serial_wishlist = wishlist.serialize()
        new_wishlist = Wishlist()
        new_wishlist.deserialize(serial_wishlist)
        self.assertEqual(new_wishlist.id, wishlist.id)
        self.assertEqual(new_wishlist.name, wishlist.name)
        self.assertEqual(new_wishlist.customer_id, wishlist.customer_id)

    def test_deserialize_with_key_error(self):
        """ Deserialize an wishlist with a KeyError """
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, {})

    def test_deserialize_with_type_error(self):
        """ Deserialize an wishlist with a TypeError """
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, [])

    def test_deserialize_product_key_error(self):
        """ Deserialize an product with a KeyError """
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, {})

    def test_deserialize_product_type_error(self):
        """ Deserialize an product with a TypeError """
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, [])

    def test_add_wishlist_product(self):
        """ Create an wishlist with an product and add it to the database """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = self._create_wishlist()
        product = self._create_product()
        wishlist.products.append(product)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(wishlist.products[0].name, product.name)

        product2 = self._create_product()
        wishlist.products.append(product2)
        wishlist.save()

        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(wishlist.products), 2)
        self.assertEqual(wishlist.products[1].name, product2.name)

    # WE DONT WANT TO EDIT THE PRODUCTS

    # def test_update_wishlist_product(self):
    #     """ Update a wishlists product """
    #     wishlists = Wishlist.all()
    #     self.assertEqual(wishlists, [])

    #     product = self._create_product()
    #     wishlist = self._create_wishlist(products=[product])
    #     wishlist.create()
    #     # Assert that it was assigned an id and shows up in the database
    #     self.assertEqual(wishlist.id, 1)
    #     wishlists = Wishlist.all()
    #     self.assertEqual(len(wishlists), 1)

    #     # Fetch it back
    #     wishlist = Wishlist.find(wishlist.id)
    #     old_product = wishlist.products[0]
    #     self.assertEqual(old_product.name, product.name)

    #     old_product.city = "XX"
    #     wishlist.save()

    #     # Fetch it back again
    #     wishlist = Wishlist.find(wishlist.id)
    #     product = wishlist.products[0]
    #     self.assertEqual(product.city, "XX")

    def test_delete_wishlist_product(self):
        """ Delete an wishlists product """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])

        product = self._create_product()
        wishlist = self._create_wishlist(products=[product])
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        product = wishlist.products[0]
        product.delete()
        wishlist.save()

        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(wishlist.products), 0)
