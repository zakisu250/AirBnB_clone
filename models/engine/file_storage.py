#!/usr/bin/python3
"""
This module serializes and deserializes JSON strings
"""
import json
from ..base_model import BaseModel
from models.user import User


class FileStorage:
    """ File storage class """

    __file = "file.json"
    __objects = {}

    def all(self):
        """ Return dict representation of all objects
        """
        return self.__objects

    def new(self, object):
        """ Creates the object with the key in __obj

        Args:
            object(obj): object to create

        """
        self.__objects[object.__class__.__name__ + '.' + str(object)] = object

    def save(self):
        """ saves or serializes the json string to file """

        with open(self.__file, 'w+') as f:
            json.dump({key: value.to_dict() for key, value in
                       self.__objects.items()}, f)

    def reload(self):
        """ recreates or deserializes json string to __obj """

        try:
            with open(self.__file, 'r') as f:
                dicts = json.loads(f.read())
                for val in dicts.values():
                    cls = val["__class__"]
                    self.new(eval(cls)(**val))
        except Exception:
            pass
