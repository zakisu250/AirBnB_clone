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

    def my_errors(self, line, num_of_args):
        """Displays error messages to user

        Args:
            line(any): gets user input using command line
            num_of_args(int): number of input arguments

        Description:
            Displays output to the use based on
            the input commands.

        """
        classes = ["BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"]

        msg = ["** class name missing **",
               "** class doesn't exist **",
               "** instance id missing **",
               "** no instance found **",
               "** attribute name missing **",
               "** value missing **"]
        if not line:
            print(msg[0])
            return 1
        args = line.split()
        if num_of_args >= 1 and args[0] not in classes:
            print(msg[1])
            return 1
        elif num_of_args == 1:
            return 0
        if num_of_args >= 2 and len(args) < 2:
            print(msg[2])
            return 1
        d = models.storage.all()

        for i in range(len(args)):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        if num_of_args >= 2 and key not in d:
            print(msg[3])
            return 1
        elif num_of_args == 2:
            return 0
        if num_of_args >= 4 and len(args) < 3:
            print(msg[4])
            return 1
        if num_of_args >= 4 and len(args) < 4:
            print(msg[5])
            return 1
        return 0

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

    def do_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating an attribute

        Args:
            line(args): receives the commands:
            <class name> <id> <attribute name> "<attribute value>"
            Example: 'update User 1234-1234-1234 my_name "Bob"'

        """
        if (self.my_errors(line, 4) == 1):
            return
        args = line.split()
        d = models.storage.all()
        for i in range(len(args[1:]) + 1):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        attr_k = args[2]
        attr_v = args[3]
        try:
            if attr_v.isdigit():
                attr_v = int(attr_v)
            elif float(attr_v):
                attr_v = float(attr_v)
        except ValueError:
            pass
        class_attr = type(d[key]).__dict__
        if attr_k in class_attr.keys():
            try:
                attr_v = type(class_attr[attr_k])(attr_v)
            except Exception:
                print("Entered wrong value type")
                return
        setattr(d[key], attr_k, attr_v)
        models.storage.save()

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
