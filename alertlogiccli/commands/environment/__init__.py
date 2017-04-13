from alertlogiccli.commands import CLIModule


class Environments(CLIModule):
    """Envrionment command module encapsulates command classes working with environment entity"""

    command = "environment"

    @classmethod
    def get_parser(cls, subparsers):
        parser_environment = subparsers.add_parser(cls.command, help="environment specific actions")
        subparsers_environment = parser_environment.add_subparsers(dest="subcommand")

        return subparsers_environment
