#!/usr/bin/env python2

import mock
import httpretty
import unittest
import sys
import os.path

sys.path.insert(0, os.path.dirname(__file__)+"/..")

import alertlogic.dynapi, alertlogic.commands

class DynAPITestCase(unittest.TestCase):
    def setUp(self):
        self.account_id = "ACCOUNT_ID"
        self.environment_id = "ENVIRONMENT_ID"
        mocked_session = mock.MagicMock()
        mocked_session.api_url = "http://mock"
        mocked_session.account = self.account_id
        alertlogic.dynapi.load(mocked_session)

class Validate(DynAPITestCase):
    @httpretty.activate
    def test_environment_not_found(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=404)
        self.assertRaises(alertlogic.commands.InvalidParameterException,
                          alertlogic.commands.Validate.environment, self.environment_id)
    
    @httpretty.activate
    def test_environment_server_error(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               status=500)
        self.assertRaises(alertlogic.commands.InvalidAPIHTTPResponse,
                          alertlogic.commands.Validate.environment, self.environment_id)
    
    @httpretty.activate
    def test_environment_invalid_response(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='INVALID_BODY',
                               status=200,
                               content_type="text/json")
        self.assertRaises(alertlogic.commands.InvalidAPIResponse,
                          alertlogic.commands.Validate.environment, self.environment_id)

class DeploymentModeTestCase(DynAPITestCase):
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
        result = alertlogic.commands.DeploymentMode.set(self.environment_id, "readonly")
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
        self.assertRaises(alertlogic.commands.InvalidAPIHTTPResponse,
                          alertlogic.commands.DeploymentMode.set, self.environment_id, "readonly")
    
    @httpretty.activate
    def test_get_ok(self):
        httpretty.register_uri(httpretty.GET,
                               "http://mock/sources/v1/{}/sources/{}".format(self.account_id, self.environment_id),
                               body='{"source": {"type": "environment", "config": {"deployment_mode": "readonly"}}}',
                               status=200,
                               content_type="text/json")
        result = alertlogic.commands.DeploymentMode.get(self.environment_id)
        assert(result == "readonly")

if __name__ == '__main__':
    unittest.main()
