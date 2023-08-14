#!/usr/bin/python3
""" Defines a base class called BaseModel """
from datetime import datetime
import uuid
import models


class BaseModel():
    """ Base class to create different classes """

    def __init__(self, *args, **kwargs):
        """ Initializes the base class with attributes

        Args:
            args(args): arguments
            kwargs(dict): key/value pair arguments for attribute and value
        """
        DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(
                            value, DATE_FORMAT)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """ Prints the string containing the class,
        the id, and the whole object """
        cl = type(self).__name__
        return ("[{}] ({}) {}".format(cl, self.id, self.__dict__))

    def save(self):
        """ Updates the public instance attribute updated_at
        with the current datetime """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ returns the __dict__ of instances in a dictionary format """
        obj_dict = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                obj_dict[key] = value.isoformat()
            else:
                obj_dict[key] = value

        obj_dict['__class__'] = self.__class__.__name__
        self.updated_at = datetime.now()
        return obj_dict
