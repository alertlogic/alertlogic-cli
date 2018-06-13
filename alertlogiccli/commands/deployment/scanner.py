from alertlogic.services import Skaletor
import alertlogiccli.command

import requests
import json

class ScannerEstimation(alertlogiccli.command.Command):
    """Command to get scanner estimation from skaletor"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("scanner_estimation", help="gets scanner estimation from skaletor")
        parser.set_defaults(command=self)
        parser.add_argument("--deployment_id", help="deployment id")
        parser.add_argument("--vpc_key", help="vpc key")

    def execute(self, context):
        args = context.get_final_args()
        skaletor = Skaletor(context.get_session())
        try:
            response = skaletor.get_scanner_estimation(
                account_id = args["account_id"],
                deployment_id = args["deployment_id"],
                vpc_key = args["vpc_key"]
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("scanner_estimation", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))