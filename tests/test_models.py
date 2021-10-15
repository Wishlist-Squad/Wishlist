"""
Test cases for Wishlist Class

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_pets.py:TestPetModel

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.wishlist import Wishlist
from service import app
from .factories import WishlistFactory

######################################################################
#  Wishlist   CLASS   T E S T   C A S E S
######################################################################
class TestWishlistModel(unittest.TestCase):
    """Test Cases for Wishlist Class"""

    # @classmethod
    # def setUpClass(cls):
    #     """This runs once before the entire test suite"""
    #     app.config["TESTING"] = True
    #     app.config["DEBUG"] = False
    #     app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    #     app.logger.setLevel(logging.CRITICAL)
    #     Pet.init_db(app)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     """This runs once after the entire test suite"""
    #     db.session.close()
    #
    # def setUp(self):
    #     """This runs before each test"""
    #     db.drop_all()  # clean up the last tests
    #     db.create_all()  # make our sqlalchemy tables
    #
    # def tearDown(self):
    #     """This runs after each test"""
    #     db.session.remove()
    #     db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """Create a wishlist and assert that it exists"""
        pet = Wishlist(name="test",customer=123456)
        self.assertTrue(pet != None)
        self.assertEqual(pet.get_name(), "test")
        self.assertEqual(pet.get_customer(), 123456)

    def test_update_a_wishlist(self):
        """Update a Wishlist"""
        wishlist = Wishlist("test",123456)
        wishlist.update_name("abcd")
        self.assertEqual(wishlist.get_name(),"abcd")
        wishlist.update_customer(654321)
        self.assertEqual(wishlist.get_customer(),654321)

    # def test_delete_a_pet(self):
    #     """Delete a Pet"""
    #     pet = PetFactory()
    #     pet.create()
    #     self.assertEqual(len(Pet.all()), 1)
    #     # delete the pet and make sure it isn't in the database
    #     pet.delete()
    #     self.assertEqual(len(Pet.all()), 0)
    #
    # def test_serialize_a_pet(self):
    #     """Test serialization of a Pet"""
    #     pet = PetFactory()
    #     data = pet.serialize()
    #     self.assertNotEqual(data, None)
    #     self.assertIn("id", data)
    #     self.assertEqual(data["id"], pet.id)
    #     self.assertIn("name", data)
    #     self.assertEqual(data["name"], pet.name)
    #     self.assertIn("category", data)
    #     self.assertEqual(data["category"], pet.category)
    #     self.assertIn("available", data)
    #     self.assertEqual(data["available"], pet.available)
    #     self.assertIn("gender", data)
    #     self.assertEqual(data["gender"], pet.gender.name)
    #
    # def test_deserialize_a_pet(self):
    #     """Test deserialization of a Pet"""
    #     data = {
    #         "id": 1,
    #         "name": "kitty",
    #         "category": "cat",
    #         "available": True,
    #         "gender": "Female",
    #     }
    #     pet = Pet()
    #     pet.deserialize(data)
    #     self.assertNotEqual(pet, None)
    #     self.assertEqual(pet.id, None)
    #     self.assertEqual(pet.name, "kitty")
    #     self.assertEqual(pet.category, "cat")
    #     self.assertEqual(pet.available, True)
    #     self.assertEqual(pet.gender, Gender.Female)
    #
    # def test_deserialize_missing_data(self):
    #     """Test deserialization of a Pet with missing data"""
    #     data = {"id": 1, "name": "kitty", "category": "cat"}
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)
    #
    # def test_deserialize_bad_data(self):
    #     """Test deserialization of bad data"""
    #     data = "this is not a dictionary"
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)
    #
    # def test_deserialize_bad_available(self):
    #     """ Test deserialization of bad available attribute """
    #     test_pet = PetFactory()
    #     data = test_pet.serialize()
    #     data["available"] = "true"
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)
    #
    # def test_deserialize_bad_gender(self):
    #     """ Test deserialization of bad gender attribute """
    #     test_pet = PetFactory()
    #     data = test_pet.serialize()
    #     data["gender"] = "male" # wrong case
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)
    #
    # def test_find_pet(self):
    #     """Find a Pet by ID"""
    #     pets = PetFactory.create_batch(3)
    #     for pet in pets:
    #         pet.create()
    #     logging.debug(pets)
    #     # make sure they got saved
    #     self.assertEqual(len(Pet.all()), 3)
    #     # find the 2nd pet in the list
    #     pet = Pet.find(pets[1].id)
    #     self.assertIsNot(pet, None)
    #     self.assertEqual(pet.id, pets[1].id)
    #     self.assertEqual(pet.name, pets[1].name)
    #     self.assertEqual(pet.available, pets[1].available)
    #
    # def test_find_by_category(self):
    #     """Find Pets by Category"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     pets = Pet.find_by_category("cat")
    #     self.assertEqual(pets[0].category, "cat")
    #     self.assertEqual(pets[0].name, "kitty")
    #     self.assertEqual(pets[0].available, False)
    #
    # def test_find_by_name(self):
    #     """Find a Pet by Name"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     pets = Pet.find_by_name("kitty")
    #     self.assertEqual(pets[0].category, "cat")
    #     self.assertEqual(pets[0].name, "kitty")
    #     self.assertEqual(pets[0].available, False)
    #
    # def test_find_by_availability(self):
    #     """Find Pets by Availability"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     Pet(name="fifi", category="dog", available=True).create()
    #     pets = Pet.find_by_availability(False)
    #     pet_list = [pet for pet in pets]
    #     self.assertEqual(len(pet_list), 1)
    #     self.assertEqual(pets[0].name, "kitty")
    #     self.assertEqual(pets[0].category, "cat")
    #     pets = Pet.find_by_availability(True)
    #     pet_list = [pet for pet in pets]
    #     self.assertEqual(len(pet_list), 2)
    #
    # def test_find_by_gender(self):
    #     """Find Pets by Gender"""
    #     Pet(name="fido", category="dog", available=True, gender=Gender.Male).create()
    #     Pet(
    #         name="kitty", category="cat", available=False, gender=Gender.Female
    #     ).create()
    #     Pet(name="fifi", category="dog", available=True, gender=Gender.Male).create()
    #     pets = Pet.find_by_gender(Gender.Female)
    #     pet_list = [pet for pet in pets]
    #     self.assertEqual(len(pet_list), 1)
    #     self.assertEqual(pets[0].name, "kitty")
    #     self.assertEqual(pets[0].category, "cat")
    #     pets = Pet.find_by_gender(Gender.Male)
    #     pet_list = [pet for pet in pets]
    #     self.assertEqual(len(pet_list), 2)
    #
    # def test_find_or_404_found(self):
    #     """Find or return 404 found"""
    #     pets = PetFactory.create_batch(3)
    #     for pet in pets:
    #         pet.create()
    #
    #     pet = Pet.find_or_404(pets[1].id)
    #     self.assertIsNot(pet, None)
    #     self.assertEqual(pet.id, pets[1].id)
    #     self.assertEqual(pet.name, pets[1].name)
    #     self.assertEqual(pet.available, pets[1].available)
    #
    # def test_find_or_404_not_found(self):
    #     """Find or return 404 NOT found"""
    #     self.assertRaises(NotFound, Pet.find_or_404, 0)
