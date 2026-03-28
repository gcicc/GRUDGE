"""Fetch weather forecasts from wttr.in (free, no API key)."""

import requests

LOCATIONS = [
    {"name": "Allentown, PA", "query": "Allentown+PA"},
    {"name": "Bristol, PA", "query": "Bristol+PA"},
    {"name": "Mays Landing, NJ", "query": "Mays+Landing+NJ"},
]


def _fetch_one(query: str, timeout: int = 5) -> str | None:
    """Fetch compact weather for one location. Returns e.g. '72F Partly cloudy'."""
    try:
        url = f"https://wttr.in/{query}?format=%t+%C"
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "GRUDGE/0.1"})
        resp.raise_for_status()
        text = resp.content.decode("utf-8").strip()
        # Convert Celsius to Fahrenheit for US locations
        if "\u00b0C" in text:
            import re

            match = re.search(r"([+-]?\d+)\u00b0C", text)
            if match:
                c = int(match.group(1))
                f = round(c * 9 / 5 + 32)
                text = text.replace(match.group(0), f"{f}\u00b0F")
        return text
    except Exception:
        return None


def fetch_weather() -> list[dict]:
    """Fetch weather for all configured locations."""
    results = []
    for loc in LOCATIONS:
        weather = _fetch_one(loc["query"])
        if weather:
            results.append({"name": loc["name"], "weather": weather})
            print(f"  [OK]   {loc['name']}: {weather}")
        else:
            print(f"  [FAIL] {loc['name']}")
    return results
