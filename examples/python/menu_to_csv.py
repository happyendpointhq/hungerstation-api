"""Export a restaurant's full priced menu to CSV.

    python menu_to_csv.py 6944 --out kudu.csv
    python menu_to_csv.py 6944 --language ar --out kudu-ar.csv

The vendor_id comes from any listing (/restaurants, /restaurants-nearby, /search). Prices
are in the menu's `currency` (SAR). Ids and prices are the same in English and Arabic;
only names and descriptions change.
"""

import argparse
import csv

from client import get

COLUMNS = ["vendor_id", "restaurant", "section_id", "section", "item_id", "item", "price",
           "currency", "calories", "description"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_id", type=int)
    parser.add_argument("--language", default="en", choices=["en", "ar"])
    parser.add_argument("--out", default="menu.csv")
    args = parser.parse_args()

    menu = get("/restaurant-menu", vendor_id=args.vendor_id, language=args.language)
    written = 0
    # utf-8-sig so Excel shows Arabic names correctly.
    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for section in menu["sections"]:
            for item in section["items"]:
                writer.writerow({
                    "vendor_id": menu["vendor_id"],
                    "restaurant": menu["name"],
                    "section_id": section["section_id"],
                    "section": section["name"],
                    "item_id": item["item_id"],
                    "item": item["name"],
                    "price": item["price"],
                    "currency": menu["currency"],
                    "calories": item.get("calories"),
                    "description": item.get("description"),
                })
                written += 1
    print(f"{menu['name']}: wrote {written} of {menu['total_items']} items to {args.out}")


if __name__ == "__main__":
    main()
