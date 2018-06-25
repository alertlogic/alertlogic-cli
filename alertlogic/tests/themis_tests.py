from alertlogic.services import Themis
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_get_role():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/themis/v1/2/roles/aws/arn/v2",
        status=200
    )
    themis = alertlogic.services.Themis(session)
    response = themis.get_role("2", "aws", "arn", "v2")
    assert (response.status_code == 200)


@httpretty.activate
def test_validate_credentials():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.POST,
        "http://test/themis/v1/validate/aws/arn",
        status=200
    )
    themis = alertlogic.services.Themis(session)
    response = themis.validate_credentials("2", "aws", "arn", "v2", "test_arn")
    assert (response.status_code == 200)