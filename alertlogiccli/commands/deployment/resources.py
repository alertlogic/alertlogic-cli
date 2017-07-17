# This module defines commands to manipulate scheduler queues for a given deployment

import alertlogiccli.command

import requests
import json

class ListDeployed(alertlogiccli.command.Command):
    """Command to list security infrastructure resources deployed to a given deployment"""
    
    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("list_deployed_resources",
                                       help="lists security infrastructure resources deployed to a given deployment")
        parser.set_defaults(command=self)

    def execute(self, context):
        args = context.get_final_args()
        launcher = context.get_services().launcher
        try:
            response = launcher.getawsresourcesbyenvironment(account_id=args["account_id"],
                                                             environment_id=args["deployment_id"])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("fetch deployed resources", e.message)
        content = response.json()
        return json.dumps(content, sort_keys=True, indent=4)
