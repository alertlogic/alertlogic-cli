from alertlogic.services import ScanScheduler
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_scan_host():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.PUT,
        "http://test/scheduler/v1/2/3/scan?assetkey=abc",
        status=200
    )
    scheduler = alertlogic.services.ScanScheduler(session)
    response = scheduler.scan_host("2", "3", "abc")
    assert (response.status_code == 200)


@httpretty.activate
def test_list_scan_assets():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/scheduler/v1/2/3/list",
        status=200
    )
    scheduler = alertlogic.services.ScanScheduler(session)
    response = scheduler.list_scan_assets("2", "3")
    assert (response.status_code == 200)


@httpretty.activate
def test_get_scan_summary():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/scheduler/v1/2/3/summary?assetkey=abc",
        status=200
    )
    scheduler = alertlogic.services.ScanScheduler(session)
    response = scheduler.get_scan_summary("2", "3", "abc")
    assert (response.status_code == 200)
