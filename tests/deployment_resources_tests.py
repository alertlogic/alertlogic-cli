import pytest
import mock
import httpretty
import json

import defaults
import mock_tools

import alertlogiccli.command
import alertlogiccli.commands.deployment.resources

LIST_RESOURCES_REPLY_JSON = {
    "account_id":
    defaults.ACCOUNT_ID,
    "environment_id":
    defaults.DEPLOYMENT_ID,
    "vpcs": [{
        "region": "REGION_ID",
        "vpc_key": "VPC_KEY",
        "subnet": {
            "resource_key": "SUBNET_KEY",
            "resource_id": "SUBNET_ID"
        },
        "launch_configuration": {
            "resource_key": "LAUNCH_CONFIGURATION_KEY",
            "resource_id": "LAUNCH_CONFIGURATION_ID"
        },
        "auto_scaling_group": {
            "resource_key": "AUTO_SCALING_GROUP_KEY",
            "resource_id": "AUTO_SCALING_GROUP_ID"
        },
        "route_table": {
            "resource_key": "ROUTE_TABLE_KEY",
            "resource_id": "ROUTE_TABLE_ID"
        },
        "security_group": {
            "resource_key": "SECURITY_GROUP_KEY",
            "resource_id": "SECURITY_GROUP_ID"
        }
    }]
}


class TestListDeployed():
    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args()
        body = json.dumps(LIST_RESOURCES_REPLY_JSON)
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/launcher/v1/{account_id}/{deployment_id}/resources".
            format(**vars(args)),
            body=body,
            status=200,
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.resources.ListDeployed().execute(context)

        expected_sorted = json.dumps(json.loads(body), sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)

        assert (expected_sorted == result_sorted)
