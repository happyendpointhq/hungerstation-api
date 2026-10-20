"""Compare one product's price across the grocery stores delivering to a point.

    python grocery_price_compare.py milk
    python grocery_price_compare.py "almarai" --lat 21.5433 --lng 39.1728   # Jeddah

Sorts by price per base unit (per litre, per kg), not shelf price, so a 2 L pack and a
1 L pack compare fairly. Sponsored stores are marked: they are placed first by the app,
not ranked by price.
"""

import argparse

from client import RIYADH, get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--lat", type=float, default=RIYADH["latitude"])
    parser.add_argument("--lng", type=float, default=RIYADH["longitude"])
    parser.add_argument("--limit", type=int, default=20, help="stores per page, 1-50")
    args = parser.parse_args()

    data = get(
        "/grocery-price-comparison",
        query=args.query,
        latitude=args.lat,
        longitude=args.lng,
        limit=args.limit,
        language="en",
    )
    rows = []
    for store in data["stores"]:
        for product in store.get("products") or []:
            rows.append((store, product))
    # A text query matches more than one kind of product ("milk" also finds condensed milk in
    # grams), so rank within each base unit rather than across litres and kilograms.
    rows.sort(key=lambda r: (
        r[1].get("base_unit") or "~",
        r[1].get("price_per_base_unit") is None,
        r[1].get("price_per_base_unit") or 0,
    ))

    print(f"{data['total']} stores carry '{data['query']}'; {len(rows)} products from this page\n")
    for store, product in rows[:25]:
        unit = product.get("base_unit") or "?"
        per_unit = product.get("price_per_base_unit")
        per_unit_text = f"{per_unit:.2f}/{unit}" if per_unit is not None else "n/a"
        was = "" if product["price"] == product.get("original_price") else f" (was {product['original_price']})"
        ad = " [ad]" if store.get("sponsored") else ""
        print(
            f"{product['price']:>7} SAR{was:<12} {per_unit_text:>10}  {product['name'][:40]:<40} "
            f"{store['name']}{ad}"
        )


if __name__ == "__main__":
    main()
