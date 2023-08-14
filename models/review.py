#!/usr/bin/python3
""" Define Review class """
from models.base_model import BaseModel


class Review(BaseModel):
    """ Creates review instance with attributes

    Attributes:
        place_id(str): foriegn key from Place class
        user_id(str): foreign key from User class
        text(str): text content of the review
    """
    place_id = ""
    user_id = ""
    text = ""
