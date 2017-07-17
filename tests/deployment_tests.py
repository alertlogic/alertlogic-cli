#!/usr/bin/env python2

import mock
import httpretty
import unittest
import sys
import os.path

sys.path.insert(0, os.path.dirname(__file__)+"/..")

import alertlogiccli.commands
import alertlogic.dynapi

class CommandTestCase(unittest.TestCase):
    def setUp(self):
        self.account_id = "ACCOUNT_ID"
        self.environment_id = "ENVIRONMENT_ID"
        mocked_session = mock.MagicMock()
        mocked_session.api_endpoint = "http://mock"
        mocked_session.account_id = self.account_id
        services = alertlogic.dynapi.Services()
        services.set_session(mocked_session)
        self.commands = alertlogiccli.commands.Commands(services)

class Validate(CommandTestCase):
    @httpretty.activate
    def test_environment_not_found(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=404)
        self.assertRaises(alertlogiccli.commands.InvalidParameter,
                          self.commands.validate_environment, self.environment_id)

    @httpretty.activate
    def test_environment_server_error(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=500)
        self.assertRaises(alertlogiccli.commands.InvalidHTTPResponse,
                          self.commands.validate_environment, self.environment_id)

    @httpretty.activate
    def test_environment_invalid_response(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='INVALID_BODY',
                               status=200,
                               content_type="text/json")
        self.assertRaises(alertlogiccli.commands.InvalidServiceResponse,
                          self.commands.validate_environment, self.environment_id)

class DeploymentModeTestCase(CommandTestCase):
    @httpretty.activate
    def test_set_ok(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='{"source": {"type": "environment"}}',
                               status=200,
                               content_type="text/json")
        httpretty.register_uri(httpretty.POST,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=200)
        result = self.commands.environment_set_deployment_mode(self.environment_id, "readonly")
        assert(result)

    @httpretty.activate
    def test_set_server_fail(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='{"source": {"type": "environment"}}',
                               status=200,
                               content_type="text/json")
        httpretty.register_uri(httpretty.POST,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=500)
        self.assertRaises(alertlogiccli.commands.InvalidHTTPResponse,
                          self.commands.environment_set_deployment_mode, self.environment_id, "readonly")

    @httpretty.activate
    def test_get_ok(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='{"source": {"type": "environment", "config": {"deployment_mode": "readonly"}}}',
                               status=200,
                               content_type="text/json")
        result = self.commands.environment_get_deployment_mode(self.environment_id)
        assert(result == "readonly")

if __name__ == '__main__':
    unittest.main()
