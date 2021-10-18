# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pet Store Service

Paths:
------
GET /pets - Returns a list all of the Pets
GET /pets/{id} - Returns the Pet with a given id number
POST /pets - creates a new Pet record in the database
PUT /pets/{id} - updates a Pet record in the database
DELETE /pets/{id} - deletes a Pet record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Wishlist, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Wishlist Demo REST API Service",
            version="1.0",
            paths=url_for("create_wishlists", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL PETS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all of the Pets"""
    app.logger.info("Request for wishlists list")
    wishlists = []
    # customer_id = request.args.get("customer_id")
    # name = request.args.get("name")
    # if category:
    #     pets = Pet.find_by_category(category)
    # elif name:
    #     pets = Pet.find_by_name(name)
    # else:
    wishlists = Wishlist.all()

    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info("Returning %d wishlists", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A PET
######################################################################
# @app.route("/pets/<int:pet_id>", methods=["GET"])
# def get_pets(pet_id):
#     """
#     Retrieve a single Pet

#     This endpoint will return a Pet based on it's id
#     """
#     app.logger.info("Request for pet with id: %s", pet_id)
#     pet = Pet.find(pet_id)
#     if not pet:
#         raise NotFound("Pet with id '{}' was not found.".format(pet_id))

#     app.logger.info("Returning pet: %s", pet.name)
#     return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a wishlist
    This endpoint will create a Pet based the data in the body that is posted
    """
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())

    wishlist.create()
    message = wishlist.serialize()
    
    location_url = url_for("create_wishlists", wishlist_id=wishlist.id, _external=True)

    app.logger.info("Wishlist with ID [%s] created.", wishlist.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# UPDATE AN EXISTING PET
######################################################################
# @app.route("/pets/<int:pet_id>", methods=["PUT"])
# def update_pets(pet_id):
#     """
#     Update a Pet

#     This endpoint will update a Pet based the body that is posted
#     """
#     app.logger.info("Request to update pet with id: %s", pet_id)
#     check_content_type("application/json")
#     pet = Pet.find(pet_id)
#     if not pet:
#         raise NotFound("Pet with id '{}' was not found.".format(pet_id))
#     pet.deserialize(request.get_json())
#     pet.id = pet_id
#     pet.update()

#     app.logger.info("Pet with ID [%s] updated.", pet.id)
#     return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PET
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Pet

    This endpoint will delete a Pet based the id specified in the path
    """
    app.logger.info("Request to delete pet with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    app.logger.info("Wishlist with ID [%s] delete complete.", wishlist_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
