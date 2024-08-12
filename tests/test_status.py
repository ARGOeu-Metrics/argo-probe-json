import unittest

from argo_probe_json.status import Status


class StatusTests(unittest.TestCase):
    def setUp(self):
        self.status = Status()

    def test_ok(self):
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_msg(), "OK - Everything is ok")
        self.assertEqual(self.status.get_code(), 0)

    def test_critical(self):
        self.status.critical("Something is critically wrong")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )

    def test_warning(self):
        self.status.warning("You have been warned")
        self.assertEqual(self.status.get_code(), 1)
        self.assertEqual(
            self.status.get_msg(), "WARNING - You have been warned"
        )

    def test_unknown(self):
        self.status.unknown("I don't know what went wrong")
        self.assertEqual(self.status.get_code(), 3)
        self.assertEqual(
            self.status.get_msg(), "UNKNOWN - I don't know what went wrong"
        )

    def test_mixed_ok_critical_statuses(self):
        self.status.critical("Something is critically wrong")
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )

    def test_mixed_ok_warning_status(self):
        self.status.warning("You have been warned")
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_code(), 1)
        self.assertEqual(
            self.status.get_msg(), "WARNING - You have been warned"
        )

    def test_mixed_ok_unknown_status(self):
        self.status.unknown("I don't know what went wrong")
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_code(), 3)
        self.assertEqual(
            self.status.get_msg(), "UNKNOWN - I don't know what went wrong"
        )

    def test_mixed_warning_critical_status(self):
        self.status.critical("Something is critically wrong")
        self.status.warning("You have been warned")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )

    def test_mixed_warning_unknown_status(self):
        self.status.unknown("I don't know what went wrong")
        self.status.warning("You have been warned")
        self.assertEqual(self.status.get_code(), 3)
        self.assertEqual(
            self.status.get_msg(), "UNKNOWN - I don't know what went wrong"
        )

    def test_mixed_critical_unknown_status(self):
        self.status.critical("Something is critically wrong")
        self.status.unknown("I don't know what went wrong")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )

    def test_mixed_ok_warning_critical_status(self):
        self.status.warning("You have been warned")
        self.status.critical("Something is critically wrong")
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )

    def test_mixed_ok_warning_unknown_critical_status(self):
        self.status.unknown("I don't know what went wrong")
        self.status.warning("You have been warned")
        self.status.critical("Something is critically wrong")
        self.status.ok("Everything is ok")
        self.assertEqual(self.status.get_code(), 2)
        self.assertEqual(
            self.status.get_msg(), "CRITICAL - Something is critically wrong"
        )
