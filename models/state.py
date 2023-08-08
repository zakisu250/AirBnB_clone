#!/usr/bin/python3
""" Define the State class """
from models.base_model import BaseModel


class State(BaseModel):
    """ Creates a state instance with attributes

    Attributes:
        name(str): name of the state instance
    """
    name = ""
