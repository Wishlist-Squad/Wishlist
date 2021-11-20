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
    """Used for a data validation errors when deserializing"""
    pass


class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Account to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Account from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)


######################################################################
#  P R O D U C T   M O D E L
######################################################################
class Product(db.Model, PersistentBase):
    """
    Class that represents a Product
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(
        db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    product_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    purchased = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "product_id": self.product_id,
            "name": self.name,
            "purchased": self.purchased
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.product_id = data["product_id"]
            self.name = data["name"]
            self.purchased = data["purchased"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained" "bad or no data"
            )
        return self


######################################################################
#  W I S H L I S T   M O D E L
######################################################################
class Wishlist(db.Model, PersistentBase):
    """
    Class that represents an Account
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    products = db.relationship('Product', backref='wishlist', lazy=True)

    def __repr__(self):
        return "<Wishlist %r id=[%s] customer=[%s]>" % (self.name, self.id, self.customer_id)

    def serialize(self):
        """ Serializes a Account into a dictionary """
        wishlist = {
            "id": self.id,
            "name": self.name,
            "customer_id": self.customer_id,
            "products": []
        }
        for product in self.products:
            wishlist['products'].append(product.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Deserializes a Account from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.customer_id = data["customer_id"]
            product_list = data.get("products")
            for json_product in product_list:
                product = Product()
                product.deserialize(json_product)
                self.products.append(product)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlist: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data"
            )
        return self

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Accounts with the given name
        Args:
            name (string): the name of the Accounts you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_customer(cls, customer_id):
        """ Returns all Wishlists associated with given customer
        Args:
            customer_id (integer): the id of the Wishlists associated
        """
        logger.info(f"Finding Wishlists for customer: {customer_id}")
        return cls.query.filter(cls.customer_id == customer_id)
