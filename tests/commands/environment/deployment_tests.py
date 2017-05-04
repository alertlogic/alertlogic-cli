#!/usr/bin/env python2

import httpretty
import json
import mock
import os.path
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import alertlogiccli.commands.environment.deployment as deployment
import alertlogic.dynapi

ACCOUNT_ID = "ACCOUNT_ID"
ENVIRONMENT_ID = "ENVIRONMENT_ID"

LIST_RESOURCES_REPLY_JSON = {
    "account_id": ACCOUNT_ID,
    "environment_id": ENVIRONMENT_ID,
    "vpcs": [
        {
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
        }
    ]
}

GET_STATUS_REPLY_JSON = {
    "environment_id": ENVIRONMENT_ID,
    "type": "aws",
    "scope": [
        {
            "key": "REGION_KEY",
            "type": "region",
            "protection_state": "completed",
            "scope": [
                {
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
                }
            ]
        }
    ]
}

class ListDeployedResourcesTestCase(unittest.TestCase):
    def setUp(self):
        mocked_session = mock.MagicMock()
        mocked_session.api_endpoint = "http://mock"
        mocked_session.account_id = ACCOUNT_ID
        services = alertlogic.dynapi.Services()
        services.set_session(mocked_session)
        self.command = deployment.ListDeployedResourcesCommand(services)

    @httpretty.activate
    def test_ok(self):
        url = "http://mock/launcher/v1/{}/{}/resources".format(ACCOUNT_ID, ENVIRONMENT_ID)
        body = json.dumps(LIST_RESOURCES_REPLY_JSON)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200, content_type="text/json")
        result = self.command.execute(account_id=ACCOUNT_ID, environment_id=ENVIRONMENT_ID)
        expected_sorted = json.dumps(json.loads(body), sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)
        self.assertEqual(expected_sorted, result_sorted, "unexpected result")

class GetDeploymentStatusTestCase(unittest.TestCase):
    def setUp(self):
        mocked_session = mock.MagicMock()
        mocked_session.api_endpoint = "http://mock"
        mocked_session.account_id = ACCOUNT_ID
        services = alertlogic.dynapi.Services()
        services.set_session(mocked_session)
        self.command = deployment.GetDeploymentStatusCommand(services)

    @httpretty.activate
    def test_ok(self):
        url = "http://mock/launcher/v1/{}/environments/{}".format(ACCOUNT_ID, ENVIRONMENT_ID)
        body = json.dumps(GET_STATUS_REPLY_JSON)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200, content_type="text/json")
        result = self.command.execute(account_id=ACCOUNT_ID, environment_id=ENVIRONMENT_ID)
        expected_sorted = json.dumps(json.loads(body), sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)
        self.assertEqual(expected_sorted, result_sorted, "unexpected result")

if __name__ == '__main__':
    unittest.main()
