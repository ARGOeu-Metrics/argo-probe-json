import math
import unittest

from argo_probe_json.analysis import check_equality, get_range, value_in_range
from argo_probe_json.exceptions import JsonException


class AnalysisTests(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(check_equality("test", "test"))
        self.assertFalse(check_equality("test", "test2"))

    def test_get_range(self):
        self.assertEqual(get_range("0:200"), (0, 200.))
        self.assertEqual(get_range("200"), (0, 200.))
        self.assertEqual(get_range(":200"), (0, 200.))
        self.assertEqual(get_range("200:400"), (200., 400.))
        self.assertEqual(get_range("200:"), (200., math.inf))

    def test_get_range_if_not_number_in_range_string(self):
        with self.assertRaises(JsonException) as context1:
            get_range("test:200")

        with self.assertRaises(JsonException) as context2:
            get_range("test")

        with self.assertRaises(JsonException) as context3:
            get_range(":test")

        with self.assertRaises(JsonException) as context4:
            get_range("test:")

        self.assertEqual(
            context1.exception.__str__(),
            "Range 'test:200' not defined properly!"
        )

        self.assertEqual(
            context2.exception.__str__(),
            "Range 'test' not defined properly!"
        )

        self.assertEqual(
            context3.exception.__str__(),
            "Range ':test' not defined properly!"
        )

        self.assertEqual(
            context4.exception.__str__(),
            "Range 'test:' not defined properly!"
        )

    def test_value_in_range(self):
        self.assertTrue(value_in_range(value=200, range_tuple=(100, 300)))
        self.assertFalse(value_in_range(value=400, range_tuple=(100, 300)))
        self.assertTrue(value_in_range(value="200", range_tuple=(100, 300)))
        self.assertFalse(value_in_range(value="400", range_tuple=(100, 300)))

    def test_value_in_range_if_not_number(self):
        with self.assertRaises(JsonException) as context:
            value_in_range(value="meh", range_tuple=(100, 300))

        self.assertEqual(
            context.exception.__str__(), "Value 'meh' is not a number!"
        )
