"""Fetch market data (Dow Jones) from Yahoo Finance. Free, no API key."""

from datetime import datetime, timezone

import requests


def fetch_dow() -> dict | None:
    """Fetch current Dow Jones quote. Returns {price, change, change_pct, timestamp}."""
    try:
        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/%5EDJI"
            "?range=1d&interval=1d"
        )
        resp = requests.get(
            url, timeout=10, headers={"User-Agent": "GRUDGE/0.1"}
        )
        resp.raise_for_status()
        data = resp.json()
        meta = data["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev_close = meta["chartPreviousClose"]
        change = price - prev_close
        change_pct = (change / prev_close) * 100
        ts = datetime.fromtimestamp(
            meta["regularMarketTime"], tz=timezone.utc
        )
        return {
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "timestamp": ts,
        }
    except Exception as e:
        print(f"  [FAIL] Dow Jones: {e}")
        return None
