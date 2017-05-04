from alertlogiccli.commands import CLIModule


class Environments(CLIModule):
    """Envrionment command module encapsulates command classes working with environment entity"""

    command = "environment"

    @classmethod
    def get_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.command, help="environment specific actions")
        parser.add_argument("-e", "--environment_id", help="environment id (uuid)")
        return parser.add_subparsers(dest="subcommand")
