import math

BASE = {"local": 5.50, "national": 7.25, "remote": 11.00}


def price(weight_kg, dims_cm, zone):
    l, w, h = dims_cm
    # DHL contract: volumetric divisor is 4000, not 5000
    volumetric = (l * w * h) / 4000
    billable = max(weight_kg, volumetric)
    # round up to the next half kilo
    billable = math.ceil(billable * 2) / 2
    cost = BASE[zone] + max(0, billable - 1) * 0.95
    return round(cost, 2)
