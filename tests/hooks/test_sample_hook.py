"""
Unittest module to test Hooks.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.hooks.test_sample_hook.TestSampleHook

"""

import logging
import os
import pytest
import requests_mock
import unittest
from unittest import mock

# Import Hook
from es_aws_provider.hooks.es_aws_hook import EsAWSHook


log = logging.getLogger(__name__)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict('os.environ', AIRFLOW_CONN_CONN_SAMPLE='http://https%3A%2F%2Fwww.httpbin.org%2F')
class TestSampleHook(unittest.TestCase):
    """
    Test Sample Hook.
    """

    @requests_mock.mock()
    def test_post(self, m):

        # Mock endpoint
        m.post('https://www.httpbin.org/', json={'data': 'mocked response'})

        # Instantiate hook
        hook = EsAWSHook(
            sample_conn_id='conn_sample',
            method='post'
        )

        # Sample Hook's run method executes an API call
        response = hook.run()

        # Retrieve response payload
        payload = response.json()

        # Assert success status code
        assert response.status_code == 200

        # Assert the API call returns expected mocked payload
        assert payload['data'] == 'mocked response'

    @requests_mock.mock()
    def test_get(self, m):

        # Mock endpoint
        m.get('https://www.httpbin.org/', json={'data': 'mocked response'})

        # Instantiate hook
        hook = EsAWSHook(
            sample_conn_id='conn_sample',
            method='get'
        )

        # Sample Hook's run method executes an API call
        response = hook.run()

        # Retrieve response payload
        payload = response.json()

        # Assert success status code
        assert response.status_code == 200

        # Assert the API call returns expected mocked payload
        assert payload['data'] == 'mocked response'


if __name__ == '__main__':
    unittest.main()
