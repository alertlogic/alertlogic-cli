import alertlogiccli.command

import requests
import json


class SetSubnet(alertlogiccli.command.Command):
    """Command to set subnet in otis"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("set_subnet", help="Sets a security subnet in otis")
        parser.set_defaults(command=self)
        parser.add_argument("--provider_id", required=True, help="Provider id of account")
        parser.add_argument("--provider_type", required=True, help="Provider type of account (aws/azure)")
        parser.add_argument("--vpc_id", required=True, help="vpc for subnet to be deployed in")
        parser.add_argument("--subnet_id", required=True, help="subnet for infrastructure to be deployed in")

    def execute(self, context):
        args = context.get_final_args()
        otis = context.get_services().otis
        try:
            new_option = {
                "name": "predefined_security_subnet",
                "scope": {
                    "provider_id": args["provider_id"],
                    "provider_type": args["provider_type"],
                    "vpc_id": args["vpc_id"]
                },
                "value": args["subnet_id"]
            }
            response = otis.write_an_option(
                account_id=args["account_id"],
                json=new_option
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("set_subnet", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))


class GetConfiguration():
    """Command to get current configuration in otis"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("get_configuration", help="Gets a list of options for an account")
        parser.set_defaults(command=self)

    def execute(self, context):
        args = context.get_final_args()
        otis = context.get_services().otis
        try:
            response = otis.list_option_values(account_id = args["account_id"])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("get_config", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))