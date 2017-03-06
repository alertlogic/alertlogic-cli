#!/usr/bin/env python2

import mock
import httpretty
import unittest
import sys
import os.path
import json

sys.path.insert(0, os.path.dirname(__file__)+"/..")

import alertlogic.auth
import alertlogic.dynapi

class DynAPITestCase(unittest.TestCase):
    def test_parse_apidoc(self):
        with mock.patch.object(alertlogic.dynapi, 'API_SERVICES', "") as mock_value:
            services = alertlogic.dynapi.Services()
            service_data = [
                {"name": "test_endpoint1", "type": "get", "url": "/test_service/endpoint1" },
                {"name": "test_endpoint2", "type": "post", "url": "/test_service/endpoint2" }
            ]
            test_service = services.parse_apidoc(service_data)
            assert(callable(test_service.test_endpoint1))
            assert(callable(test_service.test_endpoint2))
            
            # this is sort of a hack, mock tries to get a callable first before
            # doing the real call, the process of getting a callable does not capture
            # exceptions
            try:
                test_service.test_endpoint_not_found()
            except alertlogic.dynapi.InvalidEndpointCall:
                assert(True)
            else:
                assert(False)
    
    def test_endpoint(self):
        endpoint = alertlogic.dynapi.Endpoint("test_endpoint", "get", "/part1/:parameter/part2")
        assert(endpoint.parse_url({"parameter": "value1"}) == "/part1/value1/part2")
        self.assertRaises(alertlogic.dynapi.InvalidEndpointCall,
                          endpoint.parse_url, {"invalid": "invalid"})
        self.assertRaises(alertlogic.dynapi.InvalidEndpointDefinition,
                          alertlogic.dynapi.Endpoint, "test_endpoint", "invalid", "/part1/:parameter/part2")

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.username = "USERNAME"
        self.password = "PASSWORD"
        self.api_endpoint = "http://mock"
    
    @httpretty.activate
    def test_authenticate_ok(self):
        account_id = "ACCOUNT_ID"
        response_body = {"authentication": {"token": "TOKEN", "account": {"id": account_id}}}
        httpretty.register_uri(httpretty.POST,
                               "http://mock/aims/v1/authenticate",
                               status=200,
                               content_type="text/json",
                               body=json.dumps(response_body))
        session = alertlogic.auth.Session(self.api_endpoint, self.username, self.password)
        assert(session.account == account_id)
    
    @httpretty.activate
    def test_authenticate_fail_http_400(self):
        account_id = "ACCOUNT_ID"
        response_body = {"authentication": {"token": "TOKEN", "account": {"id": account_id}}}
        httpretty.register_uri(httpretty.POST,
                               "http://mock/aims/v1/authenticate",
                               status=400,
                               body=json.dumps(response_body))
        self.assertRaises(alertlogic.auth.AuthenticationException,
                          alertlogic.auth.Session, self.api_endpoint, self.username, self.password)
    
    @httpretty.activate
    def test_authenticate_fail_empty_body(self):
        httpretty.register_uri(httpretty.POST,
                               "http://mock/aims/v1/authenticate",
                               status=200,
                               content_type="text/json",
                               body="")
        self.assertRaises(alertlogic.auth.AuthenticationException,
                          alertlogic.auth.Session, self.api_endpoint, self.username, self.password)
    
if __name__ == '__main__':
    unittest.main()
