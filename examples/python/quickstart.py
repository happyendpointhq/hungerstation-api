"""Pick a Riyadh district, list the restaurants delivering to it, then read one menu.

    python quickstart.py                 # Riyadh, first district alphabetically by slug
    python quickstart.py riyadh narjis   # a specific city and district slug
"""

import sys

from client import delivery_fee, get

city = sys.argv[1] if len(sys.argv) > 1 else "riyadh"
district = sys.argv[2] if len(sys.argv) > 2 else None

# 1. District slugs. Listings take the slug, not the display name.
if district is None:
    data = get("/districts", city=city)
    print(f"{data['total']} delivery districts in {data['city']['name_en']}")
    district = data["districts"][0]["slug"]
print(f"Using district: {district}\n")

# 2. Restaurants delivering to that district, nearest first (27 a page).
listing = get("/restaurants", city=city, district=district, language="en")
for row in listing["restaurants"][:10]:
    print(
        f"{row['name'][:28]:<28} {row['rating']!s:>4} ({row['rating_count']:>5})  "
        f"{row['eta_text']} {row['eta_unit']}  fee {delivery_fee(row)}  id {row['vendor_id']}"
    )

# 3. The full priced menu of the first restaurant.
if listing["restaurants"]:
    vendor_id = listing["restaurants"][0]["vendor_id"]
    menu = get("/restaurant-menu", vendor_id=vendor_id, language="en")
    print(f"\n{menu['name']}: {menu['total_items']} items in {menu['total_sections']} sections ({menu['currency']})")
    for section in menu["sections"][:3]:
        for item in section["items"][:3]:
            print(f"  {section['name'][:22]:<22} {item['price']:>7} {menu['currency']}  {item['name']}")
