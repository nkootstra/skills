import math

from parcel import quote


class QuoteService:
    """Entry point the CLI uses to get quotes."""

    def calculate(self, carrier, weight_kg, dims_cm, zone, customer_id=None):
        return quote.calculate(carrier, weight_kg, dims_cm, zone, customer_id)

    def cheapest(self, weight_kg, dims_cm, zone, customer_id=None):
        return quote.cheapest(weight_kg, dims_cm, zone, customer_id)


def parse_dims(text):
    parts = text.lower().split("x")
    if len(parts) != 3:
        raise ValueError("dims must look like 40x30x20")
    return tuple(float(p) for p in parts)


def round_half_kilo(value):
    return math.ceil(value * 2) / 2


def legacy_zone_lookup(postcode):
    # old postcode table from before zones were passed in by the shop
    first = int(str(postcode)[:2])
    if first < 20:
        return "local"
    if first < 90:
        return "national"
    return "remote"
