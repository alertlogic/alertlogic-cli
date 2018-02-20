import mock
import argparse

import defaults

import alertlogic.region
import alertlogiccli.context


def mock_config():
    mocked_config = mock.MagicMock()
    return mocked_config


def mock_session():
    mocked_session = mock.MagicMock()
    mocked_session.region = alertlogic.region.Region(defaults.API_ENDPOINT)
    return mocked_session


def mock_credentials():
    mocked_credentials = mock.MagicMock()
    mocked_credentials.make_session = mock.MagicMock(
        return_value=mock_session()
    )
    return mocked_credentials


def make_args(additional_args={}):
    args = dict(defaults.ARGS.items() + additional_args.items())
    return argparse.Namespace(**args)


def make_context(args):
    config = mock_config()
    credentials = mock_credentials()
    context = alertlogiccli.context.Context(args, config, credentials)
    return context
