from parcel import config
from parcel.carriers import dhl, postnl, ups


def calculate(carrier, weight_kg, dims_cm, zone, customer_id=None):
    if carrier == "postnl":
        base = postnl.price(weight_kg, dims_cm, zone)
    elif carrier == "dhl":
        base = dhl.price(weight_kg, dims_cm, zone)
    elif carrier == "ups":
        base = ups.price(weight_kg, dims_cm, zone)
    else:
        raise ValueError(f"unknown carrier: {carrier}")

    surcharge = 0.0
    if not config.SKIP_SURCHARGE:
        if zone == "remote":
            if carrier == "postnl":
                surcharge = 2.00
            else:
                surcharge = 3.50
        if config.CURRENT_REGION == "eu":
            surcharge += 1.25

    total = base + surcharge
    if customer_id == "ACME-001":
        total = total * 0.90

    vat = total * config.SETTINGS["vat"]
    return {
        "carrier": carrier,
        "base": base,
        "surcharge": round(surcharge, 2),
        "net": round(total, 2),
        "vat": round(vat, 2),
        "gross": round(total + vat, 2),
    }


def cheapest(weight_kg, dims_cm, zone, customer_id=None):
    quotes = []
    for carrier in ("postnl", "dhl", "ups"):
        quotes.append(calculate(carrier, weight_kg, dims_cm, zone, customer_id))
    quotes.sort(key=lambda q: q["gross"])
    return quotes[0]


def describe(q):
    # imported here, not at the top: label imports this module
    from parcel.label import format_money
    return f"{q['carrier']}: {format_money(q['gross'])}"
