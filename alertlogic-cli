#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import logging
import logging.config
import traceback

sys.path.insert(0, os.path.dirname(__file__))


def import_dependencies():
    try:
        global requests
        import requests
    except ImportError:
        print("requests library required, install it first: pip install requests")
        return False

    try:
        global alertlogic
        import alertlogic.auth
        import alertlogic.region
        import alertlogic.service
    except ImportError:
        print("unable to find alertlogic library, check your installation")
        return False

    try:
        global alertlogiccli
        import alertlogiccli.cons
        import alertlogiccli.config
        import alertlogiccli.credentials
        import alertlogiccli.context
        import alertlogiccli.command
    except ImportError:
        print("unable to find alertlogiccli library, check your installation")
        return False

    return True


def import_commands():
    commands = []

    try:
        import alertlogiccli.commands.deployment
        commands.append(alertlogiccli.commands.deployment.metadata)
    except ImportError:
        pass

    try:
        import alertlogiccli.commands.troubleshooting
        commands.append(alertlogiccli.commands.troubleshooting.metadata)
    except ImportError:
        pass

    return commands


def make_parser(commands):
    parser = argparse.ArgumentParser(description="alertlogic cloud insight client")

    parser.add_argument(
        "-c",
        "--config_file",
        default=alertlogiccli.cons.DEFAULT_CONFIG_FILE,
        help="use a specific configuration file"
    )
    parser.add_argument(
        "-e",
        "--credentials_file",
        default=alertlogiccli.cons.DEFAULT_CREDENTIALS_FILE,
        help="use a specific credentials file"
    )
    parser.add_argument(
        "--logging_config_file",
        help="use a specific configuration file for logging"
    )
    parser.add_argument(
        "-p",
        "--profile",
        default=alertlogiccli.cons.DEFAULT_PROFILE,
        help="use a specific profile in config and credentials"
    )
    parser.add_argument(
        "--api_endpoint",
        help="alertlogic api endpoint, either: uk or us"
    )
    parser.add_argument(
        "-a",
        "--account_id",
        help="use a specific account (managed accounts only)"
    )
    parser.add_argument(
        "-d",
        "--deployment_id",
        help="deployment id used by most commands (uuid)"
    )

    subparsers = parser.add_subparsers(
        title="commands", description="valid commands"
    )

    for command in commands:
        subparser = subparsers.add_parser(command["name"], help=command["help"])
        subsubparsers = subparser.add_subparsers()
        for subcommand in command["subcommands"]:
            subcommand.configure_parser(subsubparsers)

    return parser


def run_command():
    commands = import_commands()
    parser = make_parser(commands)
    args = parser.parse_args()

    if args.logging_config_file:
        logging.config.fileConfig(args.logging_config_file)

    config = alertlogiccli.config.Config(args.config_file, args.profile)
    credentials = alertlogiccli.credentials.Credentials(args.credentials_file, args.profile)

    context = alertlogiccli.context.Context(args, config, credentials)

    return args.command.execute(context)


def main():
    if os.environ.get("DEBUG"):
        print("Running in DEBUG mode")
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not import_dependencies():
        sys.exit(2)

    try:
        result = run_command()
        print(result)
        sys.exit(0)
    except (alertlogic.auth.AuthenticationException,
            alertlogiccli.config.ConfigException,
            alertlogiccli.credentials.CredentialsException,
            alertlogiccli.command.CommandException) as e:
        print(e.message)
        sys.exit(1)
    except Exception as e:
        msg = (
            "Oops something went wrong.\n"
            "Please contact support@alertlogic.com and provide the following information:\n"
            "****************************************************************************\n"
            "{}").format(traceback.format_exc())
        print(msg)
        sys.exit(2)


if __name__ == "__main__":
    main()
