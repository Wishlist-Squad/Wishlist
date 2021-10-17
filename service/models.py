"""
This code is adapted from Prof. Rofrano 's Pet model code
"""

"""
Models for Wishlist Demo Service

All of the models are stored in this module

Models
------
Wishlist - A Wishlist used in the application

Attributes:
-----------
name (string) - the name of the wishlist
customer (string) - customer ID
products (list of string) - a list of products IDs, seperated by ';'

"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialies the SQLAlchemy app"""
    Wishlist.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


# class Gender(Enum):
#     """Enumeration of valid wishlist Genders"""
#
#     Male = 0
#     Female = 1
#     Unknown = 3


class Wishlist(db.Model):
    """
    Class that represents a Wishlist

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    app:Flask=None

    ##################################################
    # Table Schema
    ##################################################
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), primary_key=True)
    customer = db.Column(db.String(63), primary_key=True)
    products = db.Column(db.String(1000))
    # category = db.Column(db.String(63), nullable=False)
    # available = db.Column(db.Boolean(), nullable=False, default=False)
    # gender = db.Column(
    #     db.Enum(Gender), nullable=False, server_default=(Gender.Unknown.name)
    # )

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Wishlist %r of Customer %s>" % (self.name, self.customer)

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s of Customer %s", self.name, self.customer)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s of Customer %s", self.name, self.customer)
        if not self.customer:
            raise DataValidationError("Update called with empty customer field")
        if not self.name:
            raise DataValidationError("Update called with empty Name field")
        db.session.commit()

    def delete(self):
        """Removes a Wishlist from the data store"""
        logger.info("Deleting %s of Customer %s", self.name, self.customer)
        db.session.delete(self)
        db.session.commit()

    # def serialize(self) -> dict:
    #     """Serializes a Wishlist into a dictionary"""
    #     return {
    #         "name": self.name,
    #         "customer": self.customer,
    #         "products": self.products
    #     }

    # def deserialize(self, data: dict):
    #     """
    #     Deserializes a Wishlist from a dictionary
    #     Args:
    #         data (dict): A dictionary containing the Wishlist data
    #     """
    #     try:
    #         self.name = data["name"]
    #         self.customer = data["customer"]
    #         self.products = data["products"]
    #     except AttributeError as error:
    #         raise DataValidationError("Invalid attribute: " + error.args[0])
    #     except KeyError as error:
    #         raise DataValidationError("Invalid wishlist: missing " + error.args[0])
    #     except TypeError as error:
    #         raise DataValidationError(
    #             "Invalid wishlist: body of request contained bad or no data"
    #         )
    #     return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app:Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Wishlists in the database"""
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, name:str, customer:str):
        """Finds a Wishtlist by it's Name and customer

        :param name: the name of the Wishlist to find
        :type name: string

        :return: an instance with the name and customer, or None if not found
        :rtype: Wishlist

        """
        logger.info("Processing lookup for %s of customer %s", name,customer)
        return cls.query.get({"name": name, "customer": customer})

    # @classmethod
    # def find_or_404(cls, wishlist_id:int):
    #     """Find a wishlist by it's id
    #
    #     :param wishlist_id: the id of the wishlist to find
    #     :type wishlist_id: int
    #
    #     :return: an instance with the wishlist_id, or 404_NOT_FOUND if not found
    #     :rtype: wishlist
    #
    #     """
    #     logger.info("Processing lookup or 404 for id %s ...", wishlist_id)
    #     return cls.query.get_or_404(wishlist_id)

    @classmethod
    def find_by_name(cls, name:str) -> list:
        """Returns all Wishlists with the given name

        :param name: the name of the Wishlists you want to match
        :type name: str

        :return: a collection of Wishlists with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_customer(cls, customer:str) -> list:
        """Returns all of the Wishlists in a category

        :param customer: the customer whom the wishlists belong to
        :type customer: str

        :return: a collection of Wishlists of that customer
        :rtype: list

        """
        logger.info("Processing customer query for %s ...", customer)
        return cls.query.filter(cls.customer == customer)

    # @classmethod
    # def find_by_availability(cls, available:bool=True) -> list:
    #     """Returns all wishlists by their availability
    #
    #     :param available: True for wishlists that are available
    #     :type available: str
    #
    #     :return: a collection of wishlists that are available
    #     :rtype: list
    #
    #     """
    #     logger.info("Processing available query for %s ...", available)
    #     return cls.query.filter(cls.available == available)
    #
    # @classmethod
    # def find_by_gender(cls, gender:Gender=Gender.Unknown) -> list:
    #     """Returns all wishlists by their Gender
    #
    #     :param gender: values are ['Male', 'Female', 'Unknown']
    #     :type available: enum
    #
    #     :return: a collection of wishlists that are available
    #     :rtype: list
    #
    #     """
    #     logger.info("Processing gender query for %s ...", gender.name)
    #     return cls.query.filter(cls.gender == gender)
