import unittest

from parcel import config, quote


class QuoteTest(unittest.TestCase):
    def setUp(self):
        config.CURRENT_REGION = "nl"

    def tearDown(self):
        config.CURRENT_REGION = None

    def test_postnl_light_local(self):
        q = quote.calculate("postnl", 1.0, (20, 20, 10), "local")
        self.assertEqual(q["base"], 4.95)
        self.assertEqual(q["gross"], 5.99)

    def test_dhl_uses_volumetric_weight(self):
        q = quote.calculate("dhl", 1.0, (40, 30, 20), "national")
        self.assertEqual(q["base"], 12.0)

    def test_eu_region_adds_surcharge(self):
        config.CURRENT_REGION = "eu"
        q = quote.calculate("ups", 1.0, (20, 20, 10), "local")
        self.assertEqual(q["surcharge"], 1.25)

    def test_unknown_carrier(self):
        with self.assertRaises(ValueError):
            quote.calculate("fedex", 1.0, (20, 20, 10), "local")

    def test_cheapest_returns_a_quote(self):
        q = quote.cheapest(1.0, (20, 20, 10), "local")
        self.assertTrue(q)
