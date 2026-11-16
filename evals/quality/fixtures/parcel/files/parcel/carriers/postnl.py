import math

BASE = {"local": 4.95, "national": 6.95, "remote": 9.95}


def price(weight_kg, dims_cm, zone):
    l, w, h = dims_cm
    volumetric = (l * w * h) / 5000
    billable = max(weight_kg, volumetric)
    # round up to the next half kilo
    billable = math.ceil(billable * 2) / 2
    cost = BASE[zone] + max(0, billable - 2) * 0.80
    return round(cost, 2)
