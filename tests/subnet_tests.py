import httpretty
import pytest

import alertlogiccli.command
import alertlogiccli.commands.deployment.subnet
import mock_tools


class TestSetSubnet():

    @httpretty.activate
    def test_bad_request(self):
        args = mock_tools.make_args(
            {"provider_id": "123456789012", "provider_type": "aws", "vpc_id": "vpc-1", "subnet_id": "subnet-1"}
        )
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/otis/v2/{account_id}/options".
            format(**vars(args)),
            status=400
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.subnet.SetSubnet().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args(
            {"provider_id": "123456789012", "provider_type": "aws", "vpc_id": "vpc-1", "subnet_id": "subnet-1"}
        )
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/otis/v2/{account_id}/options".
            format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.subnet.SetSubnet().execute(context)

    @httpretty.activate
    def test_created(self):
        args = mock_tools.make_args(
            {"provider_id": "123456789012", "provider_type": "aws", "vpc_id": "vpc-1", "subnet_id": "subnet-1"}
        )
        httpretty.register_uri(
            httpretty.POST,
            "{api_endpoint}/otis/v2/{account_id}/options".
            format(**vars(args)),
            status=201,
            body='{'
                 '"id": "1", '
                 '"name": "predefined_security_subnet", '
                 '"scope":{"provider_type": "aws", "provider_id":"123456789012", "vpc_id": "vpc-1"}, '
                 '"value": "subnet-1"'
                 '}',
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.subnet.SetSubnet().execute(context)
        assert (result == '{'
                          '"id":"1",'
                          '"name":"predefined_security_subnet",'
                          '"scope":{"provider_id":"123456789012","provider_type":"aws","vpc_id":"vpc-1"},'
                          '"value":"subnet-1"'
                          '}')


class TestGetConfiguration():

    @httpretty.activate
    def test_bad_request(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/otis/v2/{account_id}/options".
                format(**vars(args)),
            status=400
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.subnet.GetConfiguration().execute(context)

    @httpretty.activate
    def test_server_error(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/otis/v2/{account_id}/options".
                format(**vars(args)),
            status=500
        )
        with pytest.raises(alertlogiccli.command.InvalidHTTPResponse):
            context = mock_tools.make_context(args)
            alertlogiccli.commands.deployment.subnet.GetConfiguration().execute(context)

    @httpretty.activate
    def test_created(self):
        args = mock_tools.make_args()
        httpretty.register_uri(
            httpretty.GET,
            "{api_endpoint}/otis/v2/{account_id}/options".
                format(**vars(args)),
            status=200,
            body='['
                 '{'
                 '"id": "1", '
                 '"name": "predefined_security_subnet", '
                 '"scope":{"provider_type": "aws", "provider_id":"123456789012", "vpc_id": "vpc-1"}, '
                 '"value": "subnet-1"'
                 '}'
                 ']',
            content_type="text/json"
        )
        context = mock_tools.make_context(args)
        result = alertlogiccli.commands.deployment.subnet.GetConfiguration().execute(context)
        assert (result == '['
                          '{'
                          '"id":"1",'
                          '"name":"predefined_security_subnet",'
                          '"scope":{"provider_id":"123456789012","provider_type":"aws","vpc_id":"vpc-1"},'
                          '"value":"subnet-1"'
                          '}'
                          ']')