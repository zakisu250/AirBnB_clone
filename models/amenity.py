#!/usr/bin/python3
""" Define Amenity class """
from models.base_model import BaseModel


class Amenity(BaseModel):
    """ Creates Amenity class eith attributes

    Attributes:
        name(str): amenity name
    """
    name = ""
