from alertlogic.services import Credentials
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_create_credentials():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.POST,
        "http://test/credentials/v2/2/credentials",
        status=200
    )
    credentials = alertlogic.services.Credentials(session)
    response = credentials.create_credential("2", "name", "arn")
    assert (response.status_code == 200)


@httpretty.activate
def test_delete_credentials():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.DELETE,
        "http://test/credentials/v2/2/credentials/credential_Id",
        status=200
    )
    credentials = alertlogic.services.Credentials(session)
    response = credentials.delete_credential("2", "credential_Id")
    assert (response.status_code == 200)