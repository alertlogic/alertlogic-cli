from alertlogic.services import Deployments
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test_create_deployment():
    session = mock.mock_auth()
    body = "deployment_json"
    httpretty.register_uri(
        httpretty.POST,
        "http://test/deployments/v1/2/deployments",
        status=200
    )
    deployments = alertlogic.services.Deployments(session)
    response = deployments.create_deployment("2", body)
    assert (response.status_code == 200)


@httpretty.activate
def test_delete_deployment():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.DELETE,
        "http://test/deployments/v1/2/deployments/deployment_id",
        status=204
    )
    deployments = alertlogic.services.Deployments(session)
    response = deployments.delete_deployment("2", "deployment_id")
    assert (response.status_code == 204)


@httpretty.activate
def test_get_deployment():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/deployments/v1/2/deployments/deployment_id",
        status=200
    )
    deployments = alertlogic.services.Deployments(session)
    response = deployments.get_deployment("2", "deployment_id")
    assert (response.status_code == 200)


@httpretty.activate
def test_list_deployments():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/deployments/v1/2/deployments",
        status=200
    )
    deployments = alertlogic.services.Deployments(session)
    response = deployments.list_deployments("2")
    assert (response.status_code == 200)


@httpretty.activate
def test_update_deployments():
    session = mock.mock_auth()
    update_json = "updated_deployment"
    httpretty.register_uri(
        httpretty.PUT,
        "http://test/deployments/v1/2/deployments/deployment_id",
        status=200
    )
    deployments = alertlogic.services.Deployments(session)
    response = deployments.update_deployment("2", "deployment_id", update_json)
    assert (response.status_code == 200)