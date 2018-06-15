from alertlogic.services import Sources
import alertlogic.region
import alertlogic.auth
import httpretty
import json
import mock


@httpretty.activate
def test_get_source():
    session = mock.mock_auth()
    response_body = {
        "source": {
            "config": {
                "deployment_mode": "automatic"
            }
        }
    }
    httpretty.register_uri(
        httpretty.GET,
        "http://test/sources/v1/2/sources/3",
        status=200,
        content_type="text/json",
        body=json.dumps(response_body)
    )
    sources = alertlogic.services.Sources(session)
    response = sources.get_source("2", "3")
    assert (response.json() == response_body)


@httpretty.activate
def test_get_deployment_mode():
    session = mock.mock_auth()
    response_body = {
        "source": {
            "config": {
                "deployment_mode": "automatic"
            }
        }
    }
    httpretty.register_uri(
        httpretty.GET,
        "http://test/sources/v1/2/sources/3",
        status=200,
        content_type="text/json",
        body=json.dumps(response_body)
    )
    sources = alertlogic.services.Sources(session)
    response = sources.get_deployment_mode("2", "3")
    assert (response == "automatic")


@httpretty.activate
def test_merge_sources():
    session = mock.mock_auth()
    response_body = "merged_source"
    httpretty.register_uri(
        httpretty.POST,
        "http://test/sources/v1/2/sources/3",
        status=200,
        content_type="text/json",
        body=json.dumps(response_body)
    )
    sources = alertlogic.services.Sources(session)
    response = sources.merge_sources("2", "3", response_body)
    assert (response.json() == "merged_source")


@httpretty.activate
def test_delete_source():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.DELETE,
        "http://test/sources/v1/2/sources/3",
        status=204
    )
    sources = alertlogic.services.Sources(session)
    response = sources.delete_source("2", "3")
    assert (response.status_code == 204)