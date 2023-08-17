#!/usr/bin/python3
""" Defines a base class called BaseModel """
from datetime import datetime
import uuid
import models


class BaseModel():
    """ Base class to create different classes

    Attributed:
        id(str): id created by uuid
        created_at(datetime): time of the creation
        updated_at(datetime): time of the update
    """

    def __init__(self, *args, **kwargs):
        """ Initializes the base class with attributes

        Args:
            args(args): arguments
            kwargs(dict): key/value pair arguments for attribute and value
        """
        DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

        else:
            for key, val in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(
                            val, DATE_FORMAT)
                elif key[0] == "id":
                    self.__dict__[key] = str(val)
                else:
                    self.__dict__[key] = val

    def __str__(self):
        """ Prints the string format of the class,
        the id, and the whole object """
        cl = self.__class__.__name__
        return ("[{}] ({}) {}".format(cl, self.id, self.__dict__))

    def save(self):
        """ Updates the public instance attribute updated_at
        with the current datetime """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """ returns the __dict__ of instances in a dictionary format """
        obj_dict = {}
        for key, val in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                obj_dict[key] = val.isoformat()
            else:
                obj_dict[key] = val

        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict
