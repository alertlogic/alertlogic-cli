# This module defines commands to manipulate scheduler queues for a given environment

from alertlogiccli.commands import CLICommand
from alertlogiccli.commands import InvalidHTTPResponse, InvalidParameter, InvalidServiceResponse
import requests
import json

class ListScanQueuesCommand(CLICommand):
    """List hosts in scan queues for a given environment"""
    command = "list_scan_queues"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        cmd_help = "lists hosts in scan queues for a given environment"
        parser = subparsers.add_parser(cls.command, help=cmd_help)
        parser.add_argument("--vpc_key", help="filter hosts for a given VPC")

    def execute(self, environment_id, vpc_key=None, **kwargs):
        try:
            response = self.services.scan_scheduler.listscanassets(environment_id=environment_id)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse(self.command, e.message)
        content = response.json()
        regular = group_by_vpc(content["assets"], vpc_key)
        immediate = group_by_vpc(content["immediate"], vpc_key)
        result = {"regular": regular, "immediate": immediate}
        return json.dumps(result, sort_keys=True, indent=4)

class ScanHostCommand(CLICommand):
    """Puts a host to the immediate scan queue"""
    command = "scan_host"
    def __init__(self, services):
        CLICommand.__init__(self, services)

    @classmethod
    def get_parser(cls, subparsers):
        cmd_help = "puts a host in the immediate scan queue"
        parser = subparsers.add_parser(cls.command, help=cmd_help)
        parser.add_argument("--host_key", required=True, help="a host key to put in the queue")

    def execute(self, environment_id, host_key, **kwargs):
        try:
            response = self.services.scan_scheduler.scanasset(environment_id=environment_id, asset_key=host_key)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise InvalidHTTPResponse(self.command, e.message)
        return "ok"

def group_by_vpc(assets, filter_vpc_key):
    acc = {}
    for asset in assets:
        vpc_key = asset["vpc"]
        if not filter_vpc_key or filter_vpc_key == vpc_key:
            group = acc.get(vpc_key, {"vpc": vpc_key, "hosts": []})
            group["hosts"].append(asset)
            acc[vpc_key] = group
    return acc.values()
