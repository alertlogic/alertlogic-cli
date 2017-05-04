# File defines commands to set and get deployment mode for a given environment

from alertlogiccli.commands import CLICommand
from alertlogiccli.commands import InvalidHTTPResponse, InvalidParameter, InvalidServiceResponse
import requests


class DeploymentModeBase():
    def validate_environment(self, services, environment_id):
        try:
            response = services.sources.get_source(id=environment_id)
            if response.status_code == 404:
                raise InvalidParameter("environment", environment_id, "not found")
            response.raise_for_status()
            if response.json()["source"]["type"] != "environment":
                raise InvalidParameter("environment", environment_id, "is not an environment")
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse("validate environment", e.message)
        except (KeyError, ValueError):
            raise InvalidServiceResponse("validate environment", "source.type not found", response)

        return response


class GetDeploymentModeCommand(DeploymentModeBase, CLICommand):
    """Command to get deployment mode of a given environment"""
    command = "get_deployment_mode"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        parser_get_deployment_mode = subparsers.add_parser(cls.command, help="gets environment deployment mode")

    def execute(self, environment_id=None, **kwargs):
        response = self.validate_environment(self.services, environment_id)
        try:
            mode = response.json()["source"]["config"]["deployment_mode"]
            if mode == "readonly":
                return "readonly"
            else:
                return "automatic"
        except KeyError: # json parsed but can't find specific field
            return "automatic"



class SetDeploymentModeCommand(DeploymentModeBase, CLICommand):
    """Command to set deployment mode ("readyonly" or "automatic") for a given environment"""
    command = "set_deployment_mode"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        parser_set_deployment_mode = subparsers.add_parser(cls.command, help="sets environment deployment mode")
        parser_set_deployment_mode.add_argument("-m", "--mode", required=True, choices=["readonly", "automatic"])

    def execute(self, environment_id=None, mode=None, **kwargs):
        response = self.validate_environment(self.services, environment_id)
        try:
            new_config = { "source": { "config": { "deployment_mode": mode } } }
            response = self.services.sources.merge_source(id=environment_id, json=new_config)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse("set_deployment_mode", e.message)
        return "ok"
