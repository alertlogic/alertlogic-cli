import pytest
import mock
import httpretty
import json

import defaults
import mock_tools

import alertlogiccli.command
import alertlogiccli.commands.deployment.status

GET_STATUS_REPLY_JSON = {
    "environment_id":
    defaults.DEPLOYMENT_ID,
    "type":
    "aws",
    "scope": [{
        "key":
        "REGION_KEY",
        "type":
        "region",
        "protection_state":
        "completed",
        "scope": [{
            "key": "VPC_KEY",
            "type": "vpc",
            "protection_state": "completed",
            "deployment_set": {
                "route_table_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "launch_configuration_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "security_group_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "auto_scaling_group_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "get_cidr_range": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "network_visibility_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "share_image": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "generate_key": {
                    "status": "completed",
                    "extended_info": "[]"
                },
                "security_subnet_setup": {
                    "status": "completed",
                    "extended_info": "[]"
                }
            }
        }]
    }]
}


class TestGetStatus():
    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args()
        body = json.dumps(GET_STATUS_REPLY_JSON)
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/launcher/v1/{account_id}/environments/{deployment_id}".
            format(**vars(args)),
            body=body,
            status=200,
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.status.GetStatus().execute(context)

        expected_sorted = json.dumps(json.loads(body), sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)

        assert (expected_sorted == result_sorted)
