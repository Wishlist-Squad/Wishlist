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
from service.models import Wishlist, DataValidationError, db
from service import app
from .factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  Wishlist   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlistModel(unittest.TestCase):
    """Test Cases for Wishlist Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """Create a wishlist and assert that it exists"""
        wishlist = Wishlist(name="fido", customer="1234", products="T-shirt;table")
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.name, "fido")
        self.assertEqual(wishlist.customer, "1234")
        self.assertEqual(wishlist.products, "T-shirt;table")

    def test_add_a_wishlist(self):
        """Create a wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(name="fido", customer="1234", products="T-shirt;table")
        self.assertTrue(wishlist != None)
        wishlist.create()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_update_a_wishlist(self):
        """Update a wishlist"""
        wishlist = WishlistFactory()
        logging.debug(wishlist)
        wishlist.create()
        logging.debug(wishlist)
        # Change it an save it
        wishlist.name = "k9"
        wishlist.update()
        self.assertEqual(wishlist.name, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        self.assertEqual(wishlists[0].name, "k9")

    def test_delete_a_wishlist(self):
        """Delete a wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertEqual(len(wishlist.all()), 1)
        # delete the wishlist and make sure it isn't in the database
        wishlist.delete()
        self.assertEqual(len(wishlist.all()), 0)

    # def test_serialize_a_wishlist(self):
    #     """Test serialization of a wishlist"""
    #     wishlist = WishlistFactory()
    #     data = wishlist.serialize()
    #     self.assertNotEqual(data, None)
    #     self.assertIn("id", data)
    #     self.assertEqual(data["id"], wishlist.id)
    #     self.assertIn("name", data)
    #     self.assertEqual(data["name"], wishlist.name)
    #     self.assertIn("category", data)
    #     self.assertEqual(data["category"], wishlist.category)
    #     self.assertIn("available", data)
    #     self.assertEqual(data["available"], wishlist.available)
    #     self.assertIn("gender", data)
    #     self.assertEqual(data["gender"], wishlist.gender.name)

    # def test_deserialize_a_wishlist(self):
    #     """Test deserialization of a wishlist"""
    #     data = {
    #         "id": 1,
    #         "name": "kitty",
    #         "category": "cat",
    #         "available": True,
    #         "gender": "Female",
    #     }
    #     wishlist = wishlist()
    #     wishlist.deserialize(data)
    #     self.assertNotEqual(wishlist, None)
    #     self.assertEqual(wishlist.id, None)
    #     self.assertEqual(wishlist.name, "kitty")
    #     self.assertEqual(wishlist.category, "cat")
    #     self.assertEqual(wishlist.available, True)
    #     self.assertEqual(wishlist.gender, Gender.Female)
    #
    # def test_deserialize_missing_data(self):
    #     """Test deserialization of a wishlist with missing data"""
    #     data = {"id": 1, "name": "kitty", "category": "cat"}
    #     wishlist = wishlist()
    #     self.assertRaises(DataValidationError, wishlist.deserialize, data)
    #
    # def test_deserialize_bad_data(self):
    #     """Test deserialization of bad data"""
    #     data = "this is not a dictionary"
    #     wishlist = wishlist()
    #     self.assertRaises(DataValidationError, wishlist.deserialize, data)
    #
    # def test_deserialize_bad_available(self):
    #     """ Test deserialization of bad available attribute """
    #     test_wishlist = WishlistFactory()
    #     data = test_wishlist.serialize()
    #     data["available"] = "true"
    #     wishlist = wishlist()
    #     self.assertRaises(DataValidationError, wishlist.deserialize, data)
    #
    # def test_deserialize_bad_gender(self):
    #     """ Test deserialization of bad gender attribute """
    #     test_wishlist = WishlistFactory()
    #     data = test_wishlist.serialize()
    #     data["gender"] = "male" # wrong case
    #     wishlist = wishlist()
    #     self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_find_wishlist(self):
        """Find a wishlist by name and customer"""
        wishlists = WishlistFactory.create_batch(3)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)
        # make sure they got saved
        self.assertEqual(len(wishlist.all()), 3)
        # find the 2nd wishlist in the list
        wishlist = Wishlist.find(wishlists[1].name,wishlists[1].customer)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.name, wishlists[1].name)
        self.assertEqual(wishlist.customer, wishlists[1].customer)

    def test_find_by_customer(self):
        """Find wishlists by Category"""
        Wishlist(name="fido", customer="1234").create()
        Wishlist(name="kitty", customer="4321").create()
        wishlists = Wishlist.find_by_customer("1234")
        self.assertEqual(wishlists[0].customer, "1234")
        self.assertEqual(wishlists[0].name, "fido")

    def test_find_by_name(self):
        """Find a wishlist by Name"""
        Wishlist(name="fido", customer="1234").create()
        Wishlist(name="kitty", customer="4321").create()
        wishlists = Wishlist.find_by_name("kitty")
        self.assertEqual(wishlists[0].name, "kitty")
        self.assertEqual(wishlists[0].customer, "4321")