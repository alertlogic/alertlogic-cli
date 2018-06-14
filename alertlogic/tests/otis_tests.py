from alertlogic.services import Otis
import mock
import alertlogic.region
import alertlogic.auth
import httpretty
import json

@httpretty.activate
def test_get_options():
    session = mock.mock_auth()
    response_body = [
        {
            "name": "predefined_security_subnet",
            "scope": {
                "provider_type": "aws",
                "provider_id": "1234",
                "vpc_id": "vpc-1"
            },
            "value": "subnet-1"
        }
    ]
    httpretty.register_uri(
        httpretty.GET,
        "http://test/otis/v2/2/options",
        status=200,
        content_type="text/json",
        body=json.dumps(response_body)
    )

    otis = alertlogic.services.Otis(session)
    result = otis.get_options("2")
    assert (result.json()==response_body)

@httpretty.activate
def test_get_options_fail():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/otis/v2/2/options",
        status=500
    )
    otis = alertlogic.services.Otis(session)
    result = otis.get_options("2")
    assert (result.status_code == 500)


