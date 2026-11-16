import argparse
import json
import sys

from parcel import config, label, report
from parcel.utils import QuoteService, parse_dims


def main(argv=None):
    parser = argparse.ArgumentParser(prog="parcel")
    sub = parser.add_subparsers(dest="command", required=True)

    def shipment_args(p, carrier=True):
        if carrier:
            p.add_argument("--carrier", required=True)
        p.add_argument("--weight", type=float, required=True)
        p.add_argument("--dims", required=True)
        p.add_argument("--zone", required=True, choices=["local", "national", "remote"])
        p.add_argument("--customer")
        p.add_argument("--region", default="nl", choices=["nl", "eu"])

    shipment_args(sub.add_parser("quote"))
    shipment_args(sub.add_parser("cheapest"), carrier=False)
    p_label = sub.add_parser("label")
    shipment_args(p_label)
    p_label.add_argument("--order", type=int, required=True)
    p_report = sub.add_parser("report")
    p_report.add_argument("path")
    p_report.add_argument("--region", default="nl", choices=["nl", "eu"])

    args = parser.parse_args(argv)
    config.CURRENT_REGION = args.region
    service = QuoteService()

    try:
        if args.command == "quote":
            out = service.calculate(args.carrier, args.weight, parse_dims(args.dims), args.zone, args.customer)
            print(json.dumps(out, sort_keys=True))
        elif args.command == "cheapest":
            out = service.cheapest(args.weight, parse_dims(args.dims), args.zone, args.customer)
            print(json.dumps(out, sort_keys=True))
        elif args.command == "label":
            print(label.render(args.carrier, args.weight, parse_dims(args.dims), args.zone, args.order, args.customer))
        elif args.command == "report":
            print(json.dumps(report.build(args.path), sort_keys=True))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
