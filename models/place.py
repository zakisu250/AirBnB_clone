#!/usr/bin/python3
""" Define Place class """
from models.base_model import BaseModel


class Place(BaseModel):
    """ Creates a Place instance with attributes

    Attributes:
        user_id(str): foreign key from User class
        name(str): name of the Place
        city_id(str): foreign key from City class
        description(str): description of the Place
        number_rooms(int): number of rooms of the Place, default: 0
        number_bathroomsl(int): number of bathrooms of the Place, default: 0
        max_guest(int): maximum guest of the Place, default: 0
        price_by_night(int): price per night at the Place, default 0
        latitude(float): latitude of the Place, Optional
        longitude(float): longitude of the Place, Optional
        amenity-ids(list): list of Amenity ids
    """
    user_id = ""
    name = ""
    city_id = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
