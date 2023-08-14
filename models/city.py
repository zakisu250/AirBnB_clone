#!/usr/bin/python3
""" Defines City class """
from models.base_model import BaseModel


class City(BaseModel):
    """ Creates City instance with attributes

    Attributes:
        state_id(str): foreign key from State instance
        name(str): name of the City
    """
    state_id = ""
    name = ""
