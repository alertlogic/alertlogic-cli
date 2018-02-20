import pytest
import mock
import httpretty
import json

import defaults
import mock_tools

import alertlogiccli.command
import alertlogiccli.commands.deployment.scan_queue

LIST_REPLY_JSON = {
    "assets": [{
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
    }, {
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
    }],
    "immediate": [{
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
    }]
}

LIST_EXPECTED_JSON = {
    "regular": [{
        "hosts": [{
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
        }],
        "vpc":
        "VPC1_KEY"
    }, {
        "hosts": [{
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
        }],
        "vpc":
        "VPC2_KEY"
    }],
    "immediate": [{
        "hosts": [{
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
        }],
        "vpc":
        "VPC3_KEY"
    }]
}


class TestListScanQueues():
    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args()
        body = json.dumps(LIST_REPLY_JSON)
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/scheduler/v1/{account_id}/{deployment_id}/list".
            format(**vars(args)),
            body=body,
            status=200,
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.scan_queue.ListScanQueues().execute(context)

        expected_sorted = json.dumps(LIST_EXPECTED_JSON, sort_keys=True)
        result_sorted = json.dumps(json.loads(result), sort_keys=True)

        assert (expected_sorted == result_sorted)


class ScanHostTestCase():
    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args({"asset_key": "HOST_KEY"})
        body = json.dumps(LIST_REPLY_JSON)
        httpretty.register_uri(
            httpretty.PUT,
            "{api_endpoint}/scheduler/v1/{account_id}/{deployment_id}/scan?asset={}".
            format(**vars(args)),
            status=200,
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.scan_queue.ListScanQueues().execute(context)
        assert (result == "ok")
