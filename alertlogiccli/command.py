import abc


class Command():
    """Class representing CLI command. In order to define a new command class the following needs to be done:
       Class should use CLICommand as a base class:
       1. ``add_as_subparser`` instance method needs to be defined
       2. ``execute`` instance method needs to be defined
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def configure_parser(self, subparsers):
        """Command parsers should go here
           :param subparsers: subparsers added in an argparser object
           :return: None
        """

    @abc.abstractmethod
    def execute(self, context, **kwargs):
        """Business logic should go here
           :param context: context object
        """


class CommandException(Exception):
    pass


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
