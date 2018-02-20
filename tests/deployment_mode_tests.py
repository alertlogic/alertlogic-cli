import pytest
import mock
import httpretty

import mock_tools

import alertlogiccli.command
import alertlogiccli.commands.deployment.mode


class TestGetMode():
    @httpretty.activate
    def test_not_found(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            status=404
        )
        with pytest.raises(alertlogiccli.command.InvalidParameter):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.mode.GetMode().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.mode.GetMode().execute(context)

    @httpretty.activate
    def test_invalid_response(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            body='INVALID_BODY',
            status=200,
            content_type="text/json"
        )
        with pytest.raises(alertlogiccli.command.InvalidServiceResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.mode.GetMode().execute(context)

    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            body='{"source": {"type": "environment", "config": {"deployment_mode": "readonly"}}}',
            status=200,
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.mode.GetMode().execute(context)
        assert (result == "readonly")


class TestSetMode():
    @httpretty.activate
    def test_ok(self):
        args = mock_tools.make_args(additional_args={"mode": "readonly"})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            body='{"source": {"type": "environment"}}',
            status=200,
            content_type="text/json"
        )
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            status=200
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.mode.SetMode().execute(context)
        assert (result)

    @httpretty.activate
    def test_server_fail(self):
        args = mock_tools.make_args(additional_args={"mode": "readonly"})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            body='{"source": {"type": "environment"}}',
            status=200,
            content_type="text/json"
        )
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/sources/v1/{account_id}/sources/{deployment_id}".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.mode.SetMode().execute(context)
