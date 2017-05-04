import alertlogiccli.commands
import imp
import pkgutil
import importlib
import inspect
from abc import ABCMeta, abstractmethod


class CLIModule:
    """Base class to represent comamnd line interface module
    At the moment each command belongs to a module defining scope of command.
     Each module has it's own set of input parameters defined via adding module parsers.
     In order to define a new command module class the following needs to be done:
     1. Class should use CLIModule as a base class
     2. ``command`` class attribute needs to be defined
     3. ``get_parser`` class method needs to be defined
    """
    __metaclass__ = ABCMeta
    command = "undefined_module_command"

    @abstractmethod
    def get_parser(cls, subparsers):
        """

        :param subparsers:
        :return:
        """


class CLICommand():
    """Class representing CLI command. In order to define a new command class the following needs to be done:
      1. Class should use CLICommand as a base class:
      2. ``command`` class attribute needs to be defined
      3. ``get_parser`` class method needs to be defined
      4. ``execute`` instance method needs to be defined
    """
    __metaclass__ = ABCMeta
    command = "undefined_subcommand"
    def __init__(self, services):
        self.services = services

    @abstractmethod
    def get_parser(cls, subparsers):
        """Command parsers should go here
        :param subparsers: subparsers created by module command belongs to
        :return: None
        """


    @abstractmethod
    def execute(self, **kwargs):
        """Business logic should go here
        :param args: dict with input parameters
        """


def filter_command_classes(module_path, baseClass):
    module = importlib.import_module(module_path)
    elements = dir(module)

    commands = filter(lambda x: x is not baseClass.__name__ and inspect.isclass(getattr(module, x)),
                      elements)

    return filter(lambda x: issubclass(x, baseClass),
                  map(lambda x: getattr(module, x), commands))

# import_command_modules will import all user defined modules/subcommans in alertlogic.commands package
# Function expects the following directory structure:
# alertlogic/
#           commands/ <- package in alertlogic.commands defines new command module (for example environment)
#                   command_module1/ <- inside package alertlogic.commands.command_module1 command classes are defined
#                                  get_my_command.py  <- command doing some work related to command_module1
#                                  set_my_command.py
#
#
#
#
# Function returns hash where
#   key is a tuple of 2 where first element is module ``command`` class attribute and
#     second element is subcommand ``command`` class attribute
#   value is command class object
#
def import_command_modules(subparsers):
    commands_module_path, = alertlogiccli.commands.__path__
    commands_modules = filter(lambda (loader, name, ispkg): ispkg, pkgutil.walk_packages(path=[commands_module_path]))

    commands_hash = {}

    for module in commands_modules:
        module_name = module[1]
        ### initialize command module parser
        ## single module class per command module is expected
        [ModuleClass] = filter_command_classes('alertlogiccli.commands.' + module_name, CLIModule)
        func = getattr(ModuleClass, 'get_parser')
        module_parsers = func(subparsers)
        ModuleClassCmd = getattr(ModuleClass, 'command')

        ## walk through command path and get a list of available modules
        for (module_loader, submodule_name, ispkg) in pkgutil.iter_modules(path=([commands_module_path + '/' + module_name])):
            if not ispkg:
                full_submodule_name = 'alertlogiccli.commands.' + module_name + '.' + submodule_name
                filtered_commands = filter_command_classes(full_submodule_name, CLICommand)
                for SubmoduleCmd in filtered_commands:
                    #initialize submodule parsers
                    get_parser_func = getattr(SubmoduleCmd, 'get_parser')
                    get_parser_func(module_parsers)
                    SubmoduleClassCmd = getattr(SubmoduleCmd, 'command')
                    commands_hash[(ModuleClassCmd, SubmoduleClassCmd)] = SubmoduleCmd

    return commands_hash


class CommandException(Exception): pass

class InvalidParameter(CommandException):
    def __init__(self, name, value, problem):
        super(InvalidParameter, self).__init__("{} \"{}\" {}".format(name, value, problem))

class InvalidHTTPResponse(CommandException):
    def __init__(self, trying_to, message):
        super(InvalidHTTPResponse, self).__init__("{} while trying to {}".format(message, trying_to))

class InvalidServiceResponse(CommandException):
    def __init__(self, trying_to, cause, response):
        raw = "{} while trying to {} code[ {} ] content[ {} ]"
        msg = raw.format(cause, trying_to, response.status_code, response.content)
        super(InvalidServiceResponse, self).__init__(msg)

