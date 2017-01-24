#! /usr/bin/env python2

#import api
import dynapi

import argparse

parser = argparse.ArgumentParser(description="alertlogic cloud insight client")
parser.add_argument("-p", "--profile", default="default", help="use a specific profile from your config")
subparsers = parser.add_subparsers(title="commands", description="valid commands", dest="command")

parser_environments = subparsers.add_parser("environment", help="environment specific actions")
subparsers_environments = parser_environments.add_subparsers(dest="subcommand")

parser_set_deployment_mode = subparsers_environments.add_parser("set_deployment_mode",
                                                                help="sets environment deployment mode")
parser_set_deployment_mode.add_argument("account_id", type=str)
parser_set_deployment_mode.add_argument("environment_id", type=str)
parser_set_deployment_mode.add_argument("mode", choices=["readonly", "automatic"])

args = parser.parse_args()

if args.command == "environment":
    if args.subcommand == "set_deployment_mode":
        #result = api.sources_api.set_environment_deployment_mode(args.account_id, args.environment_id, args.mode)
        dynapi.APIS.load()
        result = dynapi.DeploymentMode.set(args.account_id, args.environment_id, args.mode)
        if result:
            print("ok")
        else:
            print("failed")
