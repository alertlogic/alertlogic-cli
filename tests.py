#!/usr/bin/env python2

import mock
import unittest

import IPython

import dynapi

class DeploymentModeTestCase(unittest.TestCase):
    
    def test_set(self):
        mocked_sources = mock.MagicMock()
        get_source_fun = mocked_sources.get_source.return_value
        get_source_fun.json.return_value = {"source": {"type": "environment"}}
        merge_source_fun = mocked_sources.merge_source.return_value
        merge_source_fun.ok = True
        
        with mock.patch("dynapi.APIS.sources", mocked_sources):
            account_id = "2"
            environment_id = "0D2CD709-F70B-4584-A544-B209CEC8F99A"
            result = dynapi.DeploymentMode.set(account_id, environment_id, "readonly")
            assert(result)
            mocked_sources.get_source.assert_called_once()
            mocked_sources.merge_source.assert_called_once()

if __name__ == '__main__':
    unittest.main()
