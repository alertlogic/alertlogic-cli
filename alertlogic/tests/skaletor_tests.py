from alertlogic.services import Skaletor
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_estimation():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/skaletor/v1/2/scanners",
        status=200
    )
    skaletor = alertlogic.services.Skaletor(session)
    response = skaletor.get_scanner_estimation("2")
    assert (response.status_code == 200)
