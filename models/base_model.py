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
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    def __init__(self, *args, **kwargs):
        """ Initializes the base class with attributes

        Args:
            args(args): arguments
            kwargs(dict): key/value pair arguments for attribute and value
        """
        if args is not None and len(args) > 0:
            pass
        if kwargs:
            for key, val in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    val = datetime.strptime(val, self.DATE_FORMAT)
                if key not in ["__class__"]:
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self):
        """ Prints the string format of the class,
            the id, and the whole object """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """ Updates the public instance attribute updated_at
        with the current datetime """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ returns the __dict__ of instances in a dictionary format """
        obj_dict = {}
        for key, val in self.__dict__.items():
            if key in ["created_at", "updated_at"]:
                obj_dict[key] = val

        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
