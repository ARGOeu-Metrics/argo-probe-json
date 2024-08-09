import json
import unittest
from unittest.mock import patch

import requests
from argo_probe_json.exceptions import CriticalException
from argo_probe_json.json import Json

json1 = {
    "status": "OK",
    "tenants": {
        "EOSC": {
            "streaming": {},
            "ingest_metric": "YES"
        },
        "EOSCCORE": {
            "streaming": {},
            "ingest_metric": "NO"
        }
    }
}


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code
        self.reason = "BAD REQUEST"

    def _is_jsonable(self):
        try:
            json.dumps(self.data)
            return True

        except TypeError:
            return False

    def raise_for_status(self):
        if not str(self.status_code).startswith("2"):
            raise requests.exceptions.HTTPError(
                f"{self.status_code} {self.reason}"
            )

    def json(self):
        if isinstance(self.data, dict):
            return self.data

        else:
            raise ValueError("Bad json")


class JsonTests(unittest.TestCase):
    def setUp(self):
        self.json1 = Json(url="https://mock.url.com/some/path")

    @patch("argo_probe_json.json.requests.get")
    def test_get(self, mock_get):
        mock_get.return_value = MockResponse(data=json1, status_code=200)
        response_data = self.json1.get()
        mock_get.assert_called_once_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(response_data, json1)

    @patch("argo_probe_json.json.requests.get")
    def test_get_with_exception(self, mock_get):
        mock_get.return_value = MockResponse(data=None, status_code=400)
        with self.assertRaises(CriticalException) as context:
            self.json1.get()
        mock_get.assert_called_once_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(context.exception.__str__(), "400 BAD REQUEST")

    @patch("argo_probe_json.json.requests.get")
    def test_get_if_no_json(self, mock_get):
        mock_get.return_value = MockResponse(data=None, status_code=200)
        with self.assertRaises(CriticalException) as context:
            self.json1.get()
        mock_get.assert_called_once_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(context.exception.__str__(), "Bad json")

    @patch("argo_probe_json.json.requests.get")
    def test_parse(self, mock_get):
        mock_get.return_value = MockResponse(data=json1, status_code=200)
        value = self.json1.parse(key="status")
        mock_get.assert_called_once_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(value, "OK")

    @patch("argo_probe_json.json.requests.get")
    def test_parse_nonexisting_key(self, mock_get):
        mock_get.return_value = MockResponse(data=json1, status_code=200)
        with self.assertRaises(CriticalException) as context:
            self.json1.parse(key="nonexisting")
        mock_get.assert_called_once_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(
            context.exception.__str__(), "Key 'nonexisting' not found"
        )

    @patch("argo_probe_json.json.requests.get")
    def test_parse_nested(self, mock_get):
        mock_get.return_value = MockResponse(data=json1, status_code=200)
        value1 = self.json1.parse(key="tenants.EOSC.ingest_metric")
        value2 = self.json1.parse(key="tenants.EOSCCORE.ingest_metric")
        mock_get.assert_called_with(
            "https://mock.url.com/some/path", timeout=30
        )
        self.assertEqual(value1, "YES")
        self.assertEqual(value2, "NO")
