from alertlogic.services import Saturn
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_redeploy():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.POST,
        "http://test/saturn/v1/2/redeploy",
        status=200
    )
    saturn = alertlogic.services.Saturn(session)
    response = saturn.redeploy("2")
    assert (response.status_code == 200)


@httpretty.activate
def test_deployed_installations():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/saturn/v1/2/installations",
        status=200
    )
    saturn = alertlogic.services.Saturn(session)
    response = saturn.deployed_installations("2")
    assert (response.status_code == 200)
