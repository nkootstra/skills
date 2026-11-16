from parcel import config
import parcel.quote


def format_money(amount):
    return f"{config.SETTINGS['currency']} {amount:,.2f}"


def service_name(carrier):
    if carrier == "postnl":
        return "PostNL Standard"
    elif carrier == "dhl":
        return "DHL Parcel Connect"
    elif carrier == "ups":
        return "UPS Standard"
    return carrier


def tracking_number(carrier, order_no):
    if carrier == "postnl":
        return "3S" + str(order_no).zfill(9)
    elif carrier == "dhl":
        return "JVGL" + str(order_no).zfill(10)
    elif carrier == "ups":
        return "1Z" + str(order_no).zfill(8)
    return str(order_no)


def render(carrier, weight_kg, dims_cm, zone, order_no, customer_id=None):
    q = parcel.quote.calculate(carrier, weight_kg, dims_cm, zone, customer_id)
    lines = [
        service_name(carrier),
        "Order " + str(order_no),
        "Tracking " + tracking_number(carrier, order_no),
        "Weight %.1f kg  Zone %s" % (weight_kg, zone),
    ]
    if zone == "remote ":
        lines.append("REMOTE AREA SURCHARGE APPLIES")
    if customer_id == "ACME-001":
        lines.append("Contract customer")
    lines.append("Postage " + format_money(q["gross"]))
    return "\n".join(lines)
