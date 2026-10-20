# HungerStation API and Scraper

The HungerStation API returns Saudi food and grocery delivery data from HungerStation as
JSON: the restaurants and stores delivering to any district or coordinate, with ratings,
delivery fees, minimum orders and delivery times, full priced menus in SAR, meal deals and
offers, grocery catalogues, and one product's price compared across every store that
delivers to a point. HungerStation has no public data API, so this REST API is the way to
use its menus and prices in your own code without maintaining a HungerStation scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/hungerstation-api?utm_source=github&utm_medium=readme&utm_campaign=hungerstation-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/hungerstation1
- Product page: https://happyendpoint.com/library/hungerstation-api?utm_source=github&utm_medium=readme&utm_campaign=hungerstation-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://hungerstation1.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 37, all `GET` |
| Coverage | Saudi Arabia: every city and delivery district HungerStation serves (Riyadh, Jeddah, Dammam, Al Khobar, Mecca and more) |
| Marketplaces | Restaurants, grocery and supermarkets, HungerStation Market, pickup, flowers, pharmacies |
| Languages | English and Arabic (`language=en` or `ar`); ids and prices are the same in both |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Places**
- Cities and delivery districts with English and Arabic names and slugs
- Coordinate to city and district lookup

**Restaurants and stores**
- Every vendor delivering to a district or a coordinate, with rating and rating count, open status, delivery fee, minimum order, delivery time estimate and distance
- Four sorts (recommended, distance, rating, fastest delivery) and filters for rating, delivery time, price band, offers and more
- Search by name, dish or cuisine; themed collections; the app's home feed rails, including sponsored placements
- Every branch of a brand near a point, and the customer-voted award winners by region

**Menus and offers**
- Full priced menus with sections, descriptions, photos and calories
- The live menu at a delivery point with discounted prices, dietary info and time slots
- Item options and add-on prices, "often ordered with" items
- Meal deals, checkout offers with cap and expiry, delivery fee tiers by basket size

**Grocery**
- Grocery stores for a district, store category trees, whole catalogues and current deals
- Product search inside one store, with barcodes, pack size and price per base unit
- One product's price across every grocery store delivering to a point

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/hungerstation1). There is a free plan. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

District listings take a city slug and a district slug. Look the slugs up first:

```bash
curl "https://hungerstation1.p.rapidapi.com/districts?city=riyadh" \
  -H "x-rapidapi-host: hungerstation1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://hungerstation1.p.rapidapi.com/restaurants?city=riyadh&district=imam-mohamed-islamic-university" \
  -H "x-rapidapi-host: hungerstation1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py
```

```python
from client import get

listing = get("/restaurants", city="riyadh", district="imam-mohamed-islamic-university")
for row in listing["restaurants"]:
    print(row["name"], row["rating"], row["delivery_fee"], row["vendor_id"])

menu = get("/restaurant-menu", vendor_id=6944)
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs
```

---

## Example response

One row from `GET /restaurants?city=riyadh&district=imam-mohamed-islamic-university`,
trimmed. Values are the example in the API's public documentation. The full responses are
in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "page": 1,
    "page_size": 27,
    "has_more": true,
    "restaurants": [
      {
        "vendor_id": 188116,
        "chain_id": 104542,
        "name": "Pearl Sweet",
        "vertical": "restaurants",
        "cuisines": ["Arabic"],
        "rating": 1,
        "rating_count": 1,
        "status": "OPEN",
        "delivery_fee": 17,
        "minimum_order": 15,
        "distance": 0.4,
        "distance_unit": "km",
        "eta_text": "30 - 45",
        "eta_unit": "mins",
        "url": "https://hungerstation.com/sa-en/restaurants/regions/riyadh/imam-mohamed-islamic-university/pearl-sweet-188116"
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://hungerstation1.p.rapidapi.com`

### Places

| Endpoint | Returns |
|---|---|
| `GET /cities` | Every city HungerStation delivers in, with its slug |
| `GET /districts` | Every delivery district of a city, in English and Arabic |
| `GET /locate` | The city and district that serve a coordinate |
| `GET /cuisines` | The cuisine catalogue used to filter district listings |

### Restaurants and stores

| Endpoint | Returns |
|---|---|
| `GET /restaurants` | Restaurants delivering to a district, nearest first |
| `GET /restaurants-nearby` | Every vendor delivering to a coordinate, with a count, sorts and filters |
| `GET /listing-filters` | The filter, price band, sort and cuisine keys valid at a point |
| `GET /search` | Restaurants or stores by name, dish or cuisine |
| `GET /search-nearby` | Search at a point with a count, sorts, filters and matched dishes |
| `GET /search-suggestions` | Popular search keywords per marketplace |
| `GET /search-autocomplete` | Keyword completions for partly typed text |
| `GET /home-feed` | The app's home screen vendor rails for a location |
| `GET /collections` | Themed vendor collections (Dessert, Save More, Healthy) |
| `GET /collection-vendors` | The vendors of one collection, paged |
| `GET /brand-branches` | Every branch of one brand near a point |
| `GET /top-vendors` | Customer-voted award winners by region |
| `GET /restaurants-by-url` | The restaurants of a pasted district listing URL |

### Restaurant details and menus

| Endpoint | Returns |
|---|---|
| `GET /restaurant-details` | One restaurant's profile, price range and menu summary |
| `GET /restaurant-by-url` | The same, from a pasted restaurant URL |
| `GET /vendor-at-location` | One vendor's live card for a point, or the chain branch serving it |
| `GET /restaurant-menu` | The full priced menu, filterable by section or text |
| `GET /restaurant-menu-at-location` | The live menu for a delivery point, with discounts and time slots |
| `GET /menu-item-options` | Options, add-ons, prices and nutrition for menu items |
| `GET /frequently-ordered-with` | Suggested add-on items |
| `GET /meal-deals` | Discounted meal deals promoted at a location |
| `GET /restaurant-offers` | Discounts applied at checkout, with cap and expiry |
| `GET /delivery-fee-tiers` | Delivery fee by basket size at a point |
| `GET /restaurant-reviews` | Rating distribution and customer reviews |

### Grocery

| Endpoint | Returns |
|---|---|
| `GET /grocery-stores` | Supermarkets and grocery stores delivering to a district |
| `GET /grocery-store-details` | A store's profile, category tree and featured collections |
| `GET /grocery-store-promotions` | A store's promotion shelves with prices and offers |
| `GET /grocery-products` | Every product in one category of a store, paged |
| `GET /grocery-store-products` | A store's whole catalogue or current deals, with a total |
| `GET /grocery-product-search` | Text search inside one store |
| `GET /grocery-price-comparison` | One product's price across every store delivering to a point |
| `GET /hmarket-store` | The HungerStation Market store for a coordinate |
| `GET /status` | Service health |

---

## Things to know about the data

These come from building against the API and from a live run in north Riyadh on 20 October
2026.

- **Two kinds of listing, two shapes.** `/restaurants` (by district) returns a compact card:
  `eta_text` as a string such as `"10 - 25"`, and no promotions or sponsored flag.
  `/restaurants-nearby` (by coordinate) adds `eta_min` and `eta_max` as numbers,
  `promotions`, `incentives`, `tags`, `sponsored` and a `price_range` rank. Use the
  coordinate listing when you need offers or ads.
- **The delivery fee on a card is before promotions.** The documented nearby example shows
  `delivery_fee: 17` on a vendor whose `promotions` include "Free delivery (Spend 15 SAR)".
  Read `promotions` (and `/delivery-fee-tiers` for basket-size tiers) before you report what
  a customer pays. `client.delivery_fee()` prints both.
- **Fees vary a lot between neighbours.** In our live district listing, vendors 1 to 1.7 km
  apart charged 9, 17 or 18 SAR for delivery. Do not assume one fee per district.
- **Small rating counts are common.** Live rows included 4.0 from 4 ratings and 4.2 from 5,
  next to 4.6 from 330. Weight or filter by `rating_count` before you rank by `rating`.
- **Sponsored stores come first.** In the documented grocery comparison, the first store
  carries `"sponsored": true` and a label `"Ad"`. Ad placement is not a price ranking.
- **Compare grocery prices per base unit.** Products carry `contents` (for example 2 l),
  `price_per_base_unit` and `base_unit`. A text query matches more than one kind of product:
  "milk" returns fresh milk priced per litre and condensed milk priced per kilogram. Rank
  within one `base_unit`. `original_price` above `price` marks a discount.
- **The comparison shows at most 5 products per store** and serves only the first 200
  stores of a search (`page` times `limit` may not exceed 200).
- **Paging differs by endpoint.** `/restaurants` gives 27 rows a page (20 with
  `cuisine_id`), and an empty page in the middle of a listing can still say
  `has_more: true`, so keep paging until `has_more` is false. `/restaurants-nearby` takes
  `limit` 1 to 50; on store marketplaces keep it at 10 or more, or pages can repeat stores.
- **`vendor_id` is one branch; `chain_id` groups branches.** The same brand has a different
  `vendor_id` in every area. Use `/brand-branches` or `/vendor-at-location` to find the
  branch that serves a point.
- **Language changes names, not ids or prices.** Fetch Arabic with `language=ar` and join on
  `vendor_id` and `item_id`.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | District lookup, the restaurants delivering there, and one priced menu |
| [`examples/python/grocery_price_compare.py`](examples/python/grocery_price_compare.py) | One product across every grocery store at a point, ranked per litre or kilogram, ads marked |
| [`examples/python/menu_to_csv.py`](examples/python/menu_to_csv.py) | A restaurant's whole menu to CSV, in English or Arabic |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The best-rated vendors delivering to a point, in Node 18+ with no dependencies |
| [`samples/`](samples/) | Documented example responses for five endpoints |

---

## API or your own HungerStation scraper

A homemade HungerStation scraper has to follow the app's own feeds, which change with the
app, and it has to handle location, language and paging rules for every marketplace. This
API returns the same restaurants, menus and prices as documented JSON with a stable
contract, so the work you keep is the analysis. If you need a recurring export of a city's
menus or grocery prices rather than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=hungerstation-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query HungerStation
data without code:

```json
{
  "mcpServers": {
    "hungerstation": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: hungerstation1.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a HungerStation API?

HungerStation does not publish a public API for its restaurant, menu or price data. This
API, built and maintained by Happy Endpoint and independent of HungerStation, provides that
access as REST and JSON.

### Is this the HungerStation partner or POS integration API?

No. HungerStation's partner integrations are for restaurants receiving and managing their
own orders. This API is for reading public marketplace data: who delivers where, menus,
prices, fees and offers.

### Is there a free HungerStation API?

Yes. The RapidAPI listing has a free plan, and every endpoint can be tried on it.

### Where is the HungerStation API documentation?

Every endpoint, parameter and response is documented on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/hungerstation1), and the endpoint
table above summarises them. Example responses are in [`samples/`](samples/).

### How do I use the HungerStation API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is the client, and the
other scripts in that folder are ready to run.

### Can I scrape HungerStation menu prices?

Yes. `/restaurant-menu` returns every section and item with its price in SAR, and
[`menu_to_csv.py`](examples/python/menu_to_csv.py) writes a whole menu to CSV. For the price
at a specific delivery point, with live discounts, use `/restaurant-menu-at-location`.

### Can I compare grocery prices across stores in Riyadh or Jeddah?

Yes. `/grocery-price-comparison` takes a product and a coordinate and returns each store
delivering there with its matching products, pack size and price per base unit.
[`grocery_price_compare.py`](examples/python/grocery_price_compare.py) ranks them.

### Do you cover other Saudi and Gulf platforms?

Yes, including Aqar and Wasalt for Saudi property. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=hungerstation-api).

---

## Related repos

- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - ecommerce, grocery and price tracking data sources
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data for investment research, including consumer spending signals
- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Saudi Arabia property listings and district prices
- [wasalt-api](https://github.com/happyendpointhq/wasalt-api) - Saudi listings, REGA licences and Infath auctions

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
