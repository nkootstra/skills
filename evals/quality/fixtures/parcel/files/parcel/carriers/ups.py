import math

BASE = {"local": 6.10, "national": 7.90, "remote": 12.40}
FUEL = 0.06


def price(weight_kg, dims_cm, zone):
    l, w, h = dims_cm
    volumetric = (l * w * h) / 5000
    billable = max(weight_kg, volumetric)
    # round up to the next half kilo
    billable = math.ceil(billable * 2) / 2
    cost = BASE[zone] + max(0, billable - 1) * 0.70
    cost = cost * (1 + FUEL)
    return round(cost, 2)
