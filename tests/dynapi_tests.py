#!/usr/bin/env python2

import mock
import httpretty
import pytest
import json

import alertlogic.auth
import alertlogic.region
import alertlogic.dynapi


def test_parse_apidoc():
    with mock.patch.object(alertlogic.dynapi, 'API_SERVICES', "") as mock_value:
        services = alertlogic.dynapi.Services()
        service_data = [{
            "name": "test_endpoint1",
            "type": "get",
            "url": "/test_service/endpoint1"
        }, {
            "name": "test_endpoint2",
            "type": "post",
            "url": "/test_service/endpoint2"
        }]
        test_service = services.parse_apidoc(service_data)
        assert (callable(test_service.test_endpoint1))
        assert (callable(test_service.test_endpoint2))

        # this is sort of a hack, mock tries to get a callable first before
        # doing the real call, the process of getting a callable does not capture
        # exceptions
        try:
            test_service.test_endpoint_not_found()
        except alertlogic.dynapi.InvalidEndpointCall:
            assert (True)
        else:
            assert (False)


def test_endpoint():
    endpoint = alertlogic.dynapi.Endpoint("test_endpoint", "get", "/part1/:parameter/part2")
    assert (endpoint.parse_url({"parameter": "value1"}) == "/part1/value1/part2")
    with pytest.raises(alertlogic.dynapi.InvalidEndpointCall):
        endpoint.parse_url({"invalid": "invalid"})
    with pytest.raises(alertlogic.dynapi.InvalidEndpointDefinition):
        alertlogic.dynapi.Endpoint("test_endpoint", "invalid", "/part1/:parameter/part2")
