from alertlogic.services import Saturn
import alertlogiccli.command

import requests
import json

class InstallationStatus(alertlogiccli.command.Command):
    """Command to get installation status from saturn"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("installation_status", help="gets installation status from saturn")
        parser.set_defaults(command=self)
        parser.add_argument("--vpc_key", help="vpc key")

    def execute(self, context):
        args = context.get_final_args()
        saturn = Saturn(context.get_session())
        try:
            response = saturn.deployed_installations(
                account_id = args["account_id"],
                vpc_key = args["vpc_key"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("installation_status", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))

class Redeploy(alertlogiccli.command.Command):
    """Command to redeploy infrastructure in saturn"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("redeploy", help="redeploys infrastructure in saturn")
        parser.set_defaults(command=self)
        parser.add_argument("--deployment_id", help="deployment id")
        parser.add_argument("--vpc_key", help="vpc key")

    def execute(self, context):
        args = context.get_final_args()
        saturn = Saturn(context.get_session())
        try:
            response = saturn.redeploy(
               account_id = args["account_id"],
               deployment_id = args["deployment_id"],
               vpc_key = args["vpc_key"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("redeploy", e.message)
        return "ok"