#!/usr/bin/env python2

import httpretty
import json
import mock
import os.path
import sys
import unittest
from notebook.services.contents.handlers import sort_key

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import alertlogiccli.commands.environment.scan_queue as scan_queue
import alertlogic.dynapi

ACCOUNT_ID = "ACCOUNT_ID"
ENVIRONMENT_ID = "ENVIRONMENT_ID"

LIST_HOSTS_REPLY_JSON = {
    "assets": [
        {
            "vpc": "VPC1_KEY",
            "subnet": "SUBNET1_KEY",
            "name": "HOSTNAME1",
            "address": "10.0.0.1",
            "policy": {
                "credentials": None,
                "ports": [[1, 65535]]
            },
            "metadata": {
                "status": "idle",
                "last_scan": 0,
                "launch_time": 0,
                "priority": -1,
                "request_id": "",
                "last_heartbeat": 0
            },
            "id": "HOST1_KEY",
            "scanner": None
        },
        {
            "vpc": "VPC2_KEY",
            "subnet": "SUBNET2_KEY",
            "name": "HOSTNAME2",
            "address": "10.0.0.2",
            "policy": {
                "credentials": None,
                "ports": [[1, 65535]]
            },
            "metadata": {
                "status": "idle",
                "last_scan": 0,
                "launch_time": 0,
                "priority": -1,
                "request_id": "",
                "last_heartbeat": 0
            },
            "id": "HOST2_KEY",
            "scanner": None
        }
    ],
    "immediate": [
        {
            "vpc": "VPC3_KEY",
            "subnet": "SUBNET3_KEY",
            "name": "HOSTNAME3",
            "address": "10.0.0.3",
            "policy": {
                "credentials": None,
                "ports": [[1, 65535]]
            },
            "metadata": {
                "status": "idle",
                "last_scan": 0,
                "launch_time": 0,
                "priority": -1,
                "request_id": "",
                "last_heartbeat": 0
            },
            "id": "HOST3_KEY",
            "scanner": None
        }
    ]
}

LIST_HOSTS_RESULT_JSON = {
    "regular": [
        {
            "hosts": [
                {
                    "subnet": "SUBNET1_KEY",
                    "scanner": None,
                    "vpc": "VPC1_KEY",
                    "address": "10.0.0.1",
                    "policy": {
                        "credentials": None,
                        "ports": [[1, 65535]]
                    },
                    "metadata": {
                        "status": "idle",
                        "last_scan": 0,
                        "launch_time": 0,
                        "priority": -1,
                        "request_id": "",
                        "last_heartbeat": 0
                    },
                    "id": "HOST1_KEY",
                    "name": "HOSTNAME1"
                }
            ],
            "vpc": "VPC1_KEY"
        },
        {
            "hosts": [
                {
                    "subnet": "SUBNET2_KEY",
                    "scanner": None,
                    "vpc": "VPC2_KEY",
                    "address": "10.0.0.2",
                    "policy": {
                        "credentials": None,
                        "ports": [[1, 65535]]
                    },
                    "metadata": {
                        "status": "idle",
                        "last_scan": 0,
                        "launch_time": 0,
                        "priority": -1,
                        "request_id": "",
                        "last_heartbeat": 0
                    },
                    "id": "HOST2_KEY",
                    "name": "HOSTNAME2"
                }
            ],
            "vpc": "VPC2_KEY"
        }
    ],
    "immediate": [
        {
            "hosts": [
                {
                    "subnet": "SUBNET3_KEY",
                    "scanner": None,
                    "vpc": "VPC3_KEY",
                    "address": "10.0.0.3",
                    "policy": {
                        "credentials": None,
                        "ports": [[1, 65535]]
                    },
                    "metadata": {
                        "status": "idle",
                        "last_scan": 0,
                        "launch_time": 0,
                        "priority": -1,
                        "request_id": "",
                        "last_heartbeat": 0
                    },
                    "id": "HOST3_KEY",
                    "name": "HOSTNAME3"
                }
            ],
            "vpc": "VPC3_KEY"
        }
    ]
}

class ListScanQueuesTestCase(unittest.TestCase):
    def setUp(self):
        mocked_session = mock.MagicMock()
        mocked_session.api_endpoint = "http://mock"
        mocked_session.account_id = ACCOUNT_ID
        services = alertlogic.dynapi.Services()
        services.set_session(mocked_session)
        self.command = scan_queue.ListScanQueuesCommand(services)

    @httpretty.activate
    def test_ok(self):
        url = "http://mock/scheduler/v1/{}/{}/list".format(ACCOUNT_ID, ENVIRONMENT_ID)
        body = json.dumps(LIST_HOSTS_REPLY_JSON)
        httpretty.register_uri(httpretty.GET, url, body=body, status=200, content_type="text/json")
        result = self.command.execute(account_id=ACCOUNT_ID, environment_id=ENVIRONMENT_ID)
        expected_sorted = json.dumps(LIST_HOSTS_RESULT_JSON, sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)
        self.assertEqual(expected_sorted, result_sorted, "unexpected result")

class ScanHostTestCase(unittest.TestCase):
    def setUp(self):
        mocked_session = mock.MagicMock()
        mocked_session.api_endpoint = "http://mock"
        mocked_session.account_id = ACCOUNT_ID
        services = alertlogic.dynapi.Services()
        services.set_session(mocked_session)
        self.command = scan_queue.ScanHostCommand(services)

    @httpretty.activate
    def test_ok(self):
        url = "http://mock/scheduler/v1/{}/{}/scan?asset=HOST_KEY".format(ACCOUNT_ID, ENVIRONMENT_ID)
        httpretty.register_uri(httpretty.PUT, url, status=200, content_type="text/json")
        result = self.command.execute(account_id=ACCOUNT_ID, environment_id=ENVIRONMENT_ID, host_key="HOST_KEY")
        expected = "ok"
        self.assertEqual(expected, result, "unexpected result")

if __name__ == '__main__':
    unittest.main()
