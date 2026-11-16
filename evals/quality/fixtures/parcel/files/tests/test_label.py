import unittest
from unittest import mock

from parcel import config, label


class LabelTest(unittest.TestCase):
    def setUp(self):
        config.CURRENT_REGION = "nl"

    def test_render_asks_for_a_quote(self):
        fake = {"carrier": "dhl", "base": 1, "surcharge": 0, "net": 1, "vat": 0.21, "gross": 1.21}
        with mock.patch("parcel.quote.calculate", return_value=fake) as calc:
            label.render("dhl", 1.0, (20, 20, 10), "local", 55)
        calc.assert_called_once_with("dhl", 1.0, (20, 20, 10), "local", None)

    def test_tracking_number_formats(self):
        self.assertEqual(label.tracking_number("postnl", 42), "3S000000042")
        self.assertEqual(label.tracking_number("ups", 42), "1Z00000042")

    def test_money(self):
        self.assertEqual(label.format_money(1234.5), "EUR 1,234.50")
