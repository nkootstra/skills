# parcel

Shipping quotes, labels and a monthly report for a small webshop. Python 3.10+, standard library only.

## Usage

The command line is the public interface; the warehouse scripts call it and parse its output.

```sh
python3 -m parcel quote --carrier dhl --weight 3.2 --dims 40x30x20 --zone national
python3 -m parcel cheapest --weight 3.2 --dims 40x30x20 --zone remote --region eu
python3 -m parcel label --carrier ups --weight 1 --dims 20x20x10 --zone local --order 10432
python3 -m parcel report data/shipments.json
```

`quote`, `cheapest` and `report` print JSON. `label` prints text. Everything under `parcel/` is internal.

## Tests

```sh
python3 -m unittest discover -s tests -v
```
