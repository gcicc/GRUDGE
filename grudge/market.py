"""Fetch market data (Dow Jones) from Yahoo Finance. Free, no API key."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests

# Linux (GitHub Actions, where this runs) ships the tz database. Windows does not
# unless tzdata is installed; there we fall back to UTC and label it UTC — never a
# UTC time labelled ET, which was the original bug.
try:
    NEW_YORK: ZoneInfo | None = ZoneInfo("America/New_York")
except ZoneInfoNotFoundError:
    NEW_YORK = None


def epoch_to_et(epoch: int | float) -> datetime:
    """Convert a Unix timestamp to New York time, or UTC if no tz database."""
    utc = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return utc.astimezone(NEW_YORK) if NEW_YORK else utc


def tz_label(ts: datetime) -> str:
    """The honest label for a timestamp from epoch_to_et."""
    return "ET" if NEW_YORK and ts.tzinfo == NEW_YORK else "UTC"


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
        ts = epoch_to_et(meta["regularMarketTime"])
        return {
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "timestamp": ts,
        }
    except Exception as e:
        print(f"  [FAIL] Dow Jones: {e}")
        return None
