from alertlogic.services import Sources
import alertlogiccli.command

import requests


class Base():

    def validate_deployment(self, context):
        args = context.get_final_args()

        sources = Sources(context.get_session())
        try:
            response = sources.get_source(account_id=args["account_id"], source_id=args["deployment_id"])
            if response.status_code == 404:
                raise alertlogiccli.command.InvalidParameter("deployment", args["deployment_id"], "not found")
            response.raise_for_status()
            if response.json()["source"]["type"] != "environment":
                raise alertlogiccli.command.InvalidParameter(
                    "deployment", args["deployment_id"], "is not an deployment")
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("validate deployment", e.message)
        except (KeyError, ValueError):
            raise alertlogiccli.command.InvalidServiceResponse("validate deployment", "source.type not found", response)

        return response


class GetMode(Base, alertlogiccli.command.Command):
    """Command to get deployment mode of a given deployment"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("get_deployment_mode", help="gets deployment deployment mode")
        parser.set_defaults(command=self)

    def execute(self, context):
        response = self.validate_deployment(context)
        try:
            mode = response.json()["source"]["config"]["deployment_mode"]
            if mode == "readonly":
                return "readonly"
            else:
                return "automatic"
        except KeyError:  # json parsed but can't find specific field
            return "automatic"


class SetMode(Base, alertlogiccli.command.Command):
    """Command to set deployment mode ("readonly" or "automatic") for a given deployment"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("set_deployment_mode", help="sets deployment deployment mode")
        parser.set_defaults(command=self)
        parser.add_argument("-m", "--mode", required=True, choices=["readonly", "automatic"])

    def execute(self, context):
        args = context.get_final_args()
        sources = Sources(context.get_session())
        try:
            response = sources.set_mode(
                account_id=args["account_id"],
                deployment_id=args["deployment_id"],
                mode=args["mode"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("set_deployment_mode", e.message)
        return "ok"
