from alertlogic.services import Credentials
import alertlogiccli.command

import requests
import json


class create_credential(alertlogiccli.command.Command):
    """Command to create credential in credential service"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("create_credential", help="Creates a credential")
        parser.set_defaults(command=self)
        parser.add_argument("--name", required=True, help="Credential name")
        parser.add_argument("--arn", required=True, help="")

    def execute(self, context):
        args = context.get_final_args()
        credentials = Credentials(context.get_session())
        try:
            response = credentials.create_credential(
                account_id=args["account_id"],
                name=args["name"],
                arn=args["arn"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("create_credential", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))


class delete_credential():
    """Command to delete credential in credentials service"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("delete_credential", help="Deletes credential")
        parser.set_defaults(command=self)
        parser.add_argument("--credential_id", required=True, help="Credential id")

    def execute(self, context):
        args = context.get_final_args()
        credentials = Credentials(context.get_session())
        try:
            response = credentials.delete_credential(
                account_id = args["account_id"],
                credential_id = args["credential_id"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("delete_credential", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))