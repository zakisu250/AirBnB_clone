#!/usr/bin/python3
"""
The console v0.1:
    Creates, Updates and Deletes instances or objects """

import json
import cmd
import re
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ HBNB Command interpreter """

    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """ Terminate the command interpreter """
        return True

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def my_errors(self, line, arg_nums):
        """ Display Error messages to the user

        Args:
            line(any): reads command with readline
            arg_nums(int): number of command arguments

        Detail:
            Display output to the use based on the input
        """

        cls = ["BaseModel", "User", "State", "Place",
               "Amenity", "City", "Review"]
        msg = ["** class name missing **",
               "** class doesn't exist **",
               "** instance id missing **",
               "** no instance found **",
               "** attribute name is missing **",
               "** value is missing **"]

        if not line:
            print(msg[0])
            return 1
        args = line.split()
        if arg_nums >= 1 and args[0] not in cls:
            print(msg[1])
            return 1
        elif arg_nums == 1:
            return 0
        if arg_nums >= 2 and len(args) < 2:
            print(msg[2])
            return 1

        sd = storage.all()
        for i in range(len(args)):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        if arg_nums >= 2 and key not in sd:
            print(msg[3])
            return 1
        elif arg_nums == 2:
            return 0
        if arg_nums >= 4 and len(args) < 3:
            print(msg[4])
            return 1
        if arg_nums >= 4 and len(args) < 4:
            print(msg[5])
            return 1
        return 0

    def handle_empty_line(self, line):
        """ Removes empty line

        Args:
            line(any): no input from the command
        """
        return False

    def do_create(self, line):
        """ Creates a new instance class and print the id

        Args:
            line(args): Argument used to create instances
            Example: 'create <class> <name>'
        """
        if (self.my_errors(line, 1) == 1):
            return

        args = line.split(" ")
        obj = eval(args[0])()
        obj.save()
        print(obj.id)

    def do_show(self, line):
        """ Prints the string representation of the instance

        Args:
            line(args): Reviel the instance using "id"
            Example: 'show User USERID'
        """
        if (self.my_errors(line, 2) == 1):
            return
        args = line.split(" ")
        sd = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        print(sd[key])

    def do_destroy(self, line):
        """ Remove or delete the instance

        Args:
            line(args): Delete the User instance using "id"
            Example: 'destroy <User> <ID>'
        """
        if (self.my_errors(line, 2) == 1):
            return

        args = line.split()
        s_d = storage.all()
        if args[1][0] == '""':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        del s_d[key]
        storage.save()

    def do_all(self, line):
        """ Show all instances of particular class

        Args:
            line(args): argument use to view user
            Example: 'all' OR 'all User'
        """
        s_d = storage.all()
        if not line:
            print([str(msg) for msg in s_d.values()])
            return

        args = line.split(" ")
        if (self.my_errors(line, 1) == 1):
            return
        print([str(val) for val in s_d.values()
               if val.__class__.__name__ == args[0]])

    def do_update(self, line):
        """ Update the instance with given attribute values

        Args:
            line(args): used with commands to update the instance
            Example: 'update <User> <ID> new_name "Zaki"'
        """
        if (self.my_errors(line, 4) == 1):
            return

        args = line.split(" ")
        s_d = storage.all()
        for i in range(len(args[1:]) + 1):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        a_key = args[2]
        a_val = args[3]
        try:
            if a_val.isdigit():
                a_val = int(a_val)
            elif float(a_val):
                a_val = float(a_val)
        except ValueError:
            pass

        class_a = type(s_d[key]).__dict__
        if a_key in class_a.keys():
            try:
                a_val = type(class_a[a_key])(a_val)
            except Exception:
                print("Entered wrong value type")
                return
        setattr(s_d[key], a_key, a_val)
        storage.save()

    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in ["BaseModel", "User", "State", "Place",
                              "Amenity", "City", "Review"]:
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def default(self, line):
        """ Handles default values of the methods listed below
        <classname>.all
        <classname>.show
        <classname>.destroy
        <classname>.count
        <classname>.update

        Description:
            line: Validate and use user commands
        """
        clss = ["BaseModel", "User", "State", "City", "Amenity",
                "Place", "Review"]

        cmds = {"all": self.do_all,
                "count": self.do_count,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in clss \
                or args[1] not in cmds.keys():
            super().default(line)
            return

        if args[1] in ["all", "count"]:
            cmds[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            cmds[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            attrs = re.match(r"\"(.+?)\", (.+)", args[2])
            if attrs.groups()[1][0] == '{':
                a_dict = eval(attrs.groups()[1])
                for key, val in a_dict.items():
                    cmds[args[1]](args[0] + " " + attrs.groups()[0] +
                                  " " + key + " " + str(val))
            else:
                mor = attrs.groups()[1].split(", ")
                cmds[args[1]](args[0] + " " + attrs.groups()[0] + " " +
                              mor[0] + " " + mor[1])


if __name__ == '__main__':
    HBNBCommand().cmdloop()
