#!/usr/bin/python3
""" Defines a base class called BaseModel """
import datetime
import uuid


class BaseModel():
    """ Base class to create different classes """

    def __init__(self, id=None, created_at=None, updated_at=None):
        """ Initializes the base class

        Args:
            id(int): id created with uuid, unique for every instance
            created_at(datetime): the time the instance is created
            updated_at(datetime): the time the instance is updated
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        """ Prints the string containing the class,
        the id, and the whole object """
        cl = type(self).__name__
        return ("{} {} {}".format(cl, self.id, self.__dict__))

    def save(self):
        """ Updates the public instance attribute updated_at
        with the current datetime """
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """ returns the __dict__ of instances in a dictionary format """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__

        if 'created_at' in obj_dict:
            obj_dict['created_at'] = obj_dict['created_at'].isoformat()
        if 'updated_at' in obj_dict:
            obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()
        return obj_dict
