from alertlogic.services import AssetsQuery
import alertlogic.region
import alertlogic.auth
import httpretty
import mock


@httpretty.activate
def test():
    session = mock.mock_auth()
    httpretty.register_uri(
        httpretty.GET,
        "http://test/assets_query/v1/2/deployments/3/assets",
        status=200
    )
    assets = alertlogic.services.AssetsQuery(session)
    response = assets.get_assets_in_deployment("2", "3")
    assert (response.status_code == 200)
