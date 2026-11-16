import json

from parcel import config
from parcel import quote


def carrier_title(carrier):
    if carrier == "postnl":
        return "PostNL"
    elif carrier == "dhl":
        return "DHL"
    elif carrier == "ups":
        return "UPS"
    return carrier.upper()


def build(path):
    with open(path) as fh:
        rows = json.load(fh)

    totals = {}
    list_price = 0.0
    skipped = 0
    for row in rows:
        try:
            dims = tuple(row["dims"])
            if row.get("internal"):
                # internal transfers between our own warehouses carry no surcharges
                config.SKIP_SURCHARGE = True
            q = quote.calculate(row["carrier"], row["weight"], dims, row["zone"], row.get("customer"))
            config.SKIP_SURCHARGE = False
        except Exception:
            skipped += 1
            continue

        title = carrier_title(row["carrier"])
        entry = totals.setdefault(title, {"shipments": 0, "net": 0.0, "gross": 0.0})
        entry["shipments"] += 1
        entry["net"] = round(entry["net"] + q["net"], 2)
        entry["gross"] = round(entry["gross"] + q["gross"], 2)

        # what the shipment would have cost without the contract discount
        if row.get("customer") == "ACME-001":
            list_price += q["net"] / 0.90
        else:
            list_price += q["net"]

    return {
        "carriers": totals,
        "list_price_net": round(list_price, 2),
        "skipped": skipped,
    }
