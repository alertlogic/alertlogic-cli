from alertlogic.services import ScanScheduler
import alertlogiccli.command

import requests
import json


class ListScanQueues(alertlogiccli.command.Command):
    """List hosts in scan queues for a given deployment"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser(
            "list_scan_queues",
            help="lists hosts in scan queues for a given deployment"
        )
        parser.set_defaults(command=self)

    def execute(self, context):
        args = context.get_final_args()
        scan_scheduler = ScanScheduler(context.get_session())
        try:
            response = scan_scheduler.list_scan_assets(
                account_id=args["account_id"],
                deployment_id=args["deployment_id"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("fetch scan queues", e.message)

        content = response.json()
        regular = self.group_by_vpc(content["assets"])
        immediate = self.group_by_vpc(content["immediate"])
        result = {"regular": regular, "immediate": immediate}
        return json.dumps(result, sort_keys=True, indent=4)

    def group_by_vpc(self, assets):
        acc = {}
        for asset in assets:
            vpc_key = asset["vpc"]
            group = acc.get(vpc_key, {"vpc": vpc_key, "hosts": []})
            group["hosts"].append(asset)
            acc[vpc_key] = group
        return acc.values()


class ScanHost(alertlogiccli.command.Command):
    """Puts a host to the immediate scan queue"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("scan_host", help="puts a host in the immediate scan queue")
        parser.set_defaults(command=self)

        parser.add_argument(
            "--host_key",
            dest="asset_key",
            required=True,
            help="a host key to put in the queue"
        )

    def execute(self, context):
        args = context.get_final_args()
        scan_scheduler = ScanScheduler(context.get_session())
        try:
            response = scan_scheduler.scan_host(
                account_id=args["account_id"],
                deployment_id=args["deployment_id"],
                asset_key=args["asset_key"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("put host in scan queue", e.message)
        return "ok"
