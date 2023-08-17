#!/usr/bin/python3
"""
This module serializes and deserializes JSON strings
"""
import json
from os.path import exists
from ..base_model import BaseModel
from models.user import User
from os.path import exists
name_class = ["BaseModel", "City", "State",
              "Place", "Amenity", "Review",
              "User"]


class FileStorage:
    """ File storage class """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return dict representation of all objects
        """
        return self.__objects

    def new(self, objc):
        """ Creates the object with the key in __obj

        Args:
            objc(obj): object to create

        """
        cl = objc.__class__.__name__
        ob_id = objc.id
        cl_id = cl + "." + ob_id
        self.__objects[cl_id] = objc

    def save(self):
        """ saves or serializes the json string to file """
        a_dict = {}
        for key, val in self.__objects.items():
            a_dict[key] = val.to_dict()
        with open(self.__file_path, 'w+') as f:
            json.dump(a_dict, f)

    def reload(self):
        """ recreates or deserializes json string to __obj """
        a_dict = {}
        if (exists(self.__file_path)):
            with open(self.__file_path, 'r') as f:
                a_dict = json.load(f)
                for key, val in a_dict.items():
                    cls_name, obj_id = key.split(".")
                    if cls_name in name_class:
                        self.__objects[key] = eval(cls_name)id=obj_id, (**val)
                    else:
                        pass
