import mock
import httpretty
import pytest
import json

import alertlogic.auth
import alertlogic.region
import alertlogic.dynapi


@httpretty.activate
def test_authenticate_ok():
    response_body = {
        "authentication": {
            "token": "TOKEN",
            "account": {
                "id": "ACCOUNT_ID"
            }
        }
    }
    httpretty.register_uri(
        httpretty.POST,
        "http://mock/aims/v1/authenticate",
        status=200,
        content_type="text/json",
        body=json.dumps(response_body)
    )
    region = alertlogic.region.Region("http://mock")
    session = alertlogic.auth.Session(region, "USERNAME", "PASSWORD")
    assert (session.account_id == "ACCOUNT_ID")


@httpretty.activate
def test_authenticate_fail_http_400():
    response_body = {
        "authentication": {
            "token": "TOKEN",
            "account": {
                "id": "ACCOUNT_ID"
            }
        }
    }
    httpretty.register_uri(
        httpretty.POST,
        "http://mock/aims/v1/authenticate",
        status=400,
        body=json.dumps(response_body)
    )
    region = alertlogic.region.Region("http://mock")
    with pytest.raises(alertlogic.auth.AuthenticationException):
        session = alertlogic.auth.Session(region, "USERNAME", "PASSWORD")


@httpretty.activate
def test_authenticate_fail_empty_body():
    httpretty.register_uri(
        httpretty.POST,
        "http://mock/aims/v1/authenticate",
        status=200,
        content_type="text/json",
        body=""
    )
    region = alertlogic.region.Region("http://mock")
    with pytest.raises(alertlogic.auth.AuthenticationException):
        session = alertlogic.auth.Session(region, "USERNAME", "PASSWORD")
