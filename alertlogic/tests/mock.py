import httpretty
import alertlogic.region
import alertlogic.auth
import pytest
import json

def mock_auth():
    token = {
        "authentication": {
            "token": "TOKEN",
            "account": {
                "id": "ACCOUNT_ID"
            }
        }
    }
    httpretty.register_uri(
        httpretty.POST,
        "http://test/aims/v1/authenticate",
        status=200,
        content_type="text/json",
        body=json.dumps(token)
    )
    region = alertlogic.region.Region("http://test")
    session = alertlogic.auth.Session(region, "Username", "Password")
    return session