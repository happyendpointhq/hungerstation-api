# Sample responses

Example `200` responses for five HungerStation API endpoints, copied from the API's public
documentation. Long arrays are cut to their first two items. Field names and values are
otherwise unchanged. A live run on 20 October 2026 returned the same fields for
`/districts`, `/restaurants` and `/restaurant-menu`.

| File | Request |
|---|---|
| `districts.json` | `GET /districts?city=riyadh` |
| `restaurants.json` | `GET /restaurants?city=riyadh&district=imam-mohamed-islamic-university` |
| `restaurants-nearby.json` | `GET /restaurants-nearby?latitude=24.81338091423363&longitude=46.70321613550186` |
| `restaurant-menu.json` | `GET /restaurant-menu?vendor_id=6944` |
| `grocery-price-comparison.json` | `GET /grocery-price-comparison?query=milk&latitude=24.81338091423363&longitude=46.70321613550186` |

They are useful for writing parsers and tests before you subscribe. Live data changes
constantly, so do not hard-code these values.
