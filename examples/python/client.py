"""Minimal client for the HungerStation API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "hungerstation1.p.rapidapi.com"

# A point in north Riyadh, near Imam Muhammad Ibn Saud Islamic University.
RIYADH = {"latitude": 24.81338091423363, "longitude": 46.70321613550186}


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def delivery_fee(vendor):
    """The fee shown on a listing card is before promotions; free-delivery offers sit in
    `promotions` and need a minimum basket, so report both."""
    free = [p for p in vendor.get("promotions") or [] if p.get("type") == "FREE_DELIVERY"]
    if free:
        return f"{vendor['delivery_fee']} SAR, free over {free[0].get('minimum_order')} SAR"
    return f"{vendor['delivery_fee']} SAR"
