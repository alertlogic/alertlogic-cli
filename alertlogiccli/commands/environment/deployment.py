# This module defines commands to manipulate scheduler queues for a given environment

from alertlogiccli.commands import CLICommand
from alertlogiccli.commands import InvalidHTTPResponse, InvalidParameter, InvalidServiceResponse
import requests
import json

class ListDeployedResourcesCommand(CLICommand):
    """Command to list security infrastructure resources deployed to a given environment"""
    command = "list_deployed_resources"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        cmd_help = "lists security infrastructure resources deployed to a given environment"
        parser = subparsers.add_parser(cls.command, help=cmd_help)

    def execute(self, environment_id, **kwargs):
        try:
            response = self.services.launcher.getawsresourcesbyenvironment(environment_id=environment_id)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse(self.command, e.message)
        content = response.json()
        return json.dumps(content, sort_keys=True, indent=4)

class GetDeploymentStatusCommand(CLICommand):
    """Command to get deployment status for a given environment"""
    command = "get_deployment_status"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        cmd_help = "gets deployment status for a given environment"
        parser = subparsers.add_parser(cls.command, help=cmd_help)

    def execute(self, environment_id, **kwargs):
        try:
            response = self.services.launcher.getdeploymentstatus(environment_id=environment_id)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse(self.command, e.message)
        content = response.json()
        return json.dumps(content, sort_keys=True, indent=4)
