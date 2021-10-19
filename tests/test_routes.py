"""
Wishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_service.py:TestWishlistsServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, init_db, Wishlist, DataValidationError, db, Product
from service.routes import app
from .factories import WishlistFactory, ProductFactory

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestWishlistsServer(unittest.TestCase):
    """Wishlist Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################
    def _create_wishlists(self, count):
        """Factory method to create pets in bulk"""
        wishlists = []
        for _ in range(count):
            test_wishlist = WishlistFactory()
            resp = self.app.post(
                BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test wishlists"
            )
            new_wishlists = resp.get_json()
            test_wishlist.id = new_wishlists["id"]
            wishlists.append(test_wishlist)
        return wishlists

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Wishlist Demo REST API Service")


# LIST

    def test_get_wishlists_list(self):
        """Get a list of Wishlists"""
        self._create_wishlists(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

# GET
    def test_get_wishlist(self):
        """Get a single Wishlist"""
        # get the id of a wishlist

        wishlist = self._create_wishlists(1)[0]
        resp = self.app.get(
            f"{BASE_URL}/{wishlist.id}", content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], wishlist.name)

    def test_get_wishlist_not_found(self):
        """Get a Wishlist thats not found"""
        resp = self.app.get("/wishlists/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

# CREATE
    def test_create_wishlist(self):
        """Create a new Wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug(test_wishlist)
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"],
                         test_wishlist.name, "Names do not match")
        self.assertEqual(
            new_wishlist["customer_id"], test_wishlist.customer_id, "customer_id do not match"
        )
        self.assertEqual(
            new_wishlist["products"], test_wishlist.products, "products does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(
            f"{BASE_URL}/{new_wishlist['id']}", content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"],
                         test_wishlist.name, "Names do not match")
        self.assertEqual(
            new_wishlist["customer_id"], test_wishlist.customer_id, "customer_id do not match"
        )
        self.assertEqual(
            new_wishlist["products"], test_wishlist.products, "products does not match"
        )

    def test_create_wishlist_no_data(self):
        """Create a wishlist with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pet_wishlist_content_type(self):
        """Create a Wishlist with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # def test_create_wishlist_bad_customer_id (self):
    #     """ Create a Wishlist with bad available data """
    #     test_wishlist = WishlistFactory()
    #     logging.debug(test_wishlist)
    #     # change available to a string
    #     test_wishlist.customer_id = "bad"
    #     resp = self.app.post(
    #         BASE_URL, json=test_wishlist.serialize(), content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_pet_bad_gender(self):
    #     """ Create a Pet with bad available data """
    #     pet = PetFactory()
    #     logging.debug(pet)
    #     # change gender to a bad string
    #     test_pet = pet.serialize()
    #     test_pet["gender"] = "male"    # wrong case
    #     resp = self.app.post(
    #         BASE_URL, json=test_pet, content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# UPDATE
    def test_update_wishlist(self):
        """Update an existing Wishlist"""
        # create a wishlist to update
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the wishlist
        new_wishlist = resp.get_json()
        logging.debug(new_wishlist)
        new_wishlist["name"] = "new_name"
        resp = self.app.put(
            "/wishlists/{}".format(new_wishlist["id"]),
            json=new_wishlist,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_wishlist = resp.get_json()
        self.assertEqual(updated_wishlist["name"], "new_name")

    def test_update_bad_wishlist(self):
        """Attempt to update a non existant Wishlist"""
        test_wishlist = WishlistFactory()
        resp = self.app.put(
            f"/wishlists/{99}",
            json={},
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.get_json()[
                         "message"], "404 Not Found: Wishlist with id '99' was not found.")


# DELETE


    def test_delete_wishlist(self):
        """Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_wishlist.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
    # # make sure they are deleted
    # resp = self.app.get(
    #     "{0}/{1}".format(BASE_URL, test_wishlist.id), content_type=CONTENT_TYPE_JSON
    # )
    # self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

# QUERY

    # def test_query_pet_list_by_category(self):
    #     """Query Pets by Category"""
    #     pets = self._create_pets(10)
    #     test_category = pets[0].category
    #     category_pets = [pet for pet in pets if pet.category == test_category]
    #     resp = self.app.get(
    #         BASE_URL, query_string="category={}".format(quote_plus(test_category))
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     data = resp.get_json()
    #     self.assertEqual(len(data), len(category_pets))
    #     # check the data just to be sure
    #     for pet in data:
    #         self.assertEqual(pet["category"], test_category)

    # @patch('service.routes.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get(BASE_URL, query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch('service.routes.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get(BASE_URL, query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)

# ADD ITEM TO WISHLIST

    def test_add_product(self):
        """ Add an item to a wishlist """
        test_wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/wishlists/{}/items".format(test_wishlist.id),
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["wishlist_id"], test_wishlist.id)

# GET ITEM FROM WISHLIST

    def test_get_product(self):
        """ Get an item from a wishlist """
        # create a known wishlist
        test_wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/wishlists/{}/items".format(test_wishlist.id), 
            json=product.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # retrieve it back
        resp = self.app.get(
            "/wishlists/{}/items/{}".format(test_wishlist.id, product_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["wishlist_id"], test_wishlist.id)
