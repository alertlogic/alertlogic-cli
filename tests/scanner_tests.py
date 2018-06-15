import httpretty
import pytest

import alertlogiccli.command
import alertlogiccli.commands.deployment.scanner
import mock_tools


class TestScanner():

    @httpretty.activate
    def test_not_found(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/skaletor/v1/{account_id}/scanners?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=404
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.scanner.ScannerEstimation().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/skaletor/v1/{account_id}/scanners?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.scanner.ScannerEstimation().execute(context)

    @httpretty.activate
    def test_created(self):
        args = mock_tools.make_args({"vpc_key": None})
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/skaletor/v1/{account_id}/scanners?deployment_id=:deployment_id&vpc_key=:vpc_key".
            format(**vars(args)),
            status=200,
            body='{'
                 '"count":1,'
                 '"scanners":['
                 '{'
                 '"account_id":"010000001",'
                 '"deployment_id":"582C62B4-9D1D-4F1C-9117-BE4198198861",'
                 '"vpc_key":"/aws/us-west-1/vpc/vpc-123456",'
                 '"scaling_policy":"small",'
                 '"num_scanners_required":1'
                 '}'
                 ']'
                 '}',
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.scanner.ScannerEstimation().execute(context)
        assert (result == '{'
                          '"count":1,'
                          '"scanners":['
                          '{'
                          '"account_id":"010000001",'
                          '"deployment_id":"582C62B4-9D1D-4F1C-9117-BE4198198861",'
                          '"num_scanners_required":1,'
                          '"scaling_policy":"small",'
                          '"vpc_key":"/aws/us-west-1/vpc/vpc-123456"'
                          '}'
                          ']'
                          '}')
