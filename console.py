#!/usr/bin/python3
"""Class HBNBComand a program called console.py
"""

import cmd
import json
import re
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review}


class HBNBCommand(cmd.Cmd):
    """ hbnb command interpreter """
    prompt = '(hbnb) '

    def do_EOF(self, line):
        """ End of file"""
        print()
        return True

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def emptyline(self):
        """don´t execute nothing """
        pass

    def do_create(self, args):
        """ Creates a new instance """
        if not (args):
            print("** class name missing **")
        elif args not in classes:
            print("** class doesn't exist **")
        else:
            instance = eval(args)()
            instance.save()
            print(instance.id)

    def do_show(self, args):
        """ Prints str representation of an instance """
        if not (args):
            print("** class name missing **")
        else:
            args = args.split()
            if len(args) != 2:
                print("** instance id missing **")
            elif args[0] not in classes:
                print("** class doesn't exist **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, line):
        """ Deletes an instance based on the class name and id """
        args = line.split()
        if not line:
            print("** class name missing **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        sd = models.storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in sd:
            del sd[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """ Prints all str representation of all instances """
        split_args = args.split()
        n_list = []
        dict_json = models.storage.all()

        if not args:
            for key in dict_json:
                n_list.append(str(dict_json[key]))
            print(n_list)
        else:
            if split_args[0] in classes:
                cl_name = split_args[0] + '.'
                cl_obj = {k: v for k, v in dict_json.items() if cl_name in k}
                for key in cl_obj:
                    n_list.append(str(cl_obj[key]))
                print(n_list)
            else:
                print("** class doesn't exist **")

    def do_update(self, args):
        """ Updates an instance based on the class name and id """
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            sd = models.storage.all()
            if len(args) > 1:
                key = args[0] + '.' + args[1]
                if key in sd:
                    if len(args) > 2:
                        if len(args) > 3:
                            setattr(sd[key], args[2], args[3])
                            sd[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_count(self, args):
        """ Counts the instances of a class """
        split_args = args.split()
        if len(split_args) == 0 or split_args[0] not in classes:
            print("** class name missing **")
        else:
            cl_name = split_args[0] + "."
            cl_count = sum(1 for key in models.storage.all() if cl_name in key)
            print(cl_count)

    def default(self, line):
        """ Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)
        """
        clss = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]

        cmnds = {"all": self.do_all,
                 "count": self.do_count,
                 "show": self.do_show,
                 "destroy": self.do_destroy,
                 "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in clss:
            super().default(line)
            return

        if args[1] in cmnds.keys():
            if args[1] == "all":
                cmnds[args[1]](args[0])
            else:
                if "(" in args[2] and ")" in args[2]:
                    args[2] = args[2][1:-1]
                cmnds[args[1]](args[0] + ' ' + args[2])
        else:
            super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
