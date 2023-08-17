#!/usr/bin/python3
"""
This module serializes and deserializes JSON strings
"""
import json
from os.path import exists
from ..base_model import BaseModel
from models.user import User
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
        self.__objects[cl.id] = objc

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
        self.__objects = {}
        if (exists(self.__file_path)):
            with open(self.__file_path, 'r') as f:
                a_dict = json.loads(f)
                for key, val in a_dict.items():
                    cls_name = key.split(".")[0]
                    if cls_name in name_class:
                        self.__objetcs[key] = eval(cls_name)(**val)
                    else:
                        pass
