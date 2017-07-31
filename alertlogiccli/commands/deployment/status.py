import alertlogiccli.command

import requests
import json

class GetStatus(alertlogiccli.command.Command):
    """Command to get deployment status for a given deployment"""
    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("get_status", help="gets status for a given deployment")
        parser.set_defaults(command=self)
    
    def execute(self, context):
        args = context.get_final_args()
        launcher = context.get_services().launcher
        try:
            response = launcher.getdeploymentstatus(account_id=args["account_id"],
                                                    environment_id=args["deployment_id"])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("fetch deployment status", e.message)
        content = response.json()
        return json.dumps(content, sort_keys=True, indent=4)
