import httpretty
import pytest

import alertlogiccli.command
import alertlogiccli.commands.deployment.installation
import mock_tools


class TestInstallationStatus():

    @httpretty.activate
    def test_not_found(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/saturn/v1/{account_id}/installations?vpc_key=:vpc_key".
            format(**vars(args)),
            status=404
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.installation.InstallationStatus().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/saturn/v1/{account_id}/installations?vpc_key=:vpc_key".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.installation.InstallationStatus().execute(context)

    @httpretty.activate
    def test_created(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/saturn/v1/{account_id}/installations?vpc_key=:vpc_key".
            format(**vars(args)),
            status=200,
            body='['
                 '{'
                 '"account_id":"010000001",'
                 '"deployment_id":"582C62B4-9D1D-4F1C-9117-BE4198198861",'
                 '"vpc_key":"/aws/us-west-1/vpc/vpc-123456"'
                 '}'
                 ']',
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.installation.InstallationStatus().execute(context)
        assert (result == '['
                          '{'
                          '"account_id":"010000001",'
                          '"deployment_id":"582C62B4-9D1D-4F1C-9117-BE4198198861",'
                          '"vpc_key":"/aws/us-west-1/vpc/vpc-123456"'
                          '}'
                          ']')

class TestRedeploy():

    @httpretty.activate
    def test_not_found(self):
        args = mock_tools.make_args({"deployment_id": None, "vpc_key": None})
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/saturn/v1/{account_id}/redeploy?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=404
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.installation.Redeploy().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args({"deployment_id": None, "vpc_key": None})
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/saturn/v1/{account_id}/redeploy?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.installation.Redeploy().execute(context)

    @httpretty.activate
    def test_created(self):
        args = mock_tools.make_args({"deployment_id": None, "vpc_key": None})
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/saturn/v1/{account_id}/redeploy?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=204,
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.installation.Redeploy().execute(context)
        assert (result == "ok")