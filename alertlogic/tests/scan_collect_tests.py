from alertlogic.services import ScanCollect
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_get_id():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/scancollect/v1_remediation/2/3/appliance_vmserver_id/app_id",
        status=200
    )
    scancollect = alertlogic.services.ScanCollect(session)
    response = scancollect.get_appliance_vmserver_id("2", "3", "app_id")
    assert (response.status_code == 200)
