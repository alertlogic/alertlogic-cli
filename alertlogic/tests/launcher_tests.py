from alertlogic.services import Launcher
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_list_deployed():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/launcher/v1/2/3/resources",
        status=200
    )
    launcher = alertlogic.services.Launcher(session)
    response = launcher.list_deployed("2", "3")
    assert (response.status_code == 200)


@httpretty.activate
def test_deployment_status():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/launcher/v1/2/environments/3",
        status=200
    )
    launcher = alertlogic.services.Launcher(session)
    response = launcher.deployment_status("2", "3")
    assert (response.status_code == 200)
