"""GRUDGE entry point: fetch -> dedupe -> score -> rewrite -> build -> write."""

from pathlib import Path

from grudge.feeds import NEWS_FEEDS, PORTFOLIO_FEEDS, TECH_FEEDS, fetch_feed
from grudge.html_builder import build_page
from grudge.market import fetch_dow
from grudge.rewriter import rewrite_headline
from grudge.scorer import rank_headlines
from grudge.weather import fetch_weather


def dedupe(headlines: list[dict]) -> list[dict]:
    """Remove exact duplicate titles."""
    seen: set[str] = set()
    unique = []
    for h in headlines:
        key = h["title"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(h)
    return unique


def _fetch_section(feeds: list[dict]) -> list[dict]:
    """Fetch all feeds in a section."""
    results = []
    for f in feeds:
        results.extend(fetch_feed(f["name"], f["url"]))
    return results


def main() -> None:
    # Fetch news
    print("=== NEWS FEEDS ===")
    news_raw = _fetch_section(NEWS_FEEDS)
    news_unique = dedupe(news_raw)
    news_ranked = rank_headlines(news_unique, limit=25)
    for h in news_ranked:
        h["title"] = rewrite_headline(h["title"])
    print(f"News: {len(news_raw)} raw -> {len(news_unique)} unique -> {len(news_ranked)} selected")

    # Fetch tech/AI
    print("\n=== TECH & AI FEEDS ===")
    tech_raw = _fetch_section(TECH_FEEDS)
    tech_unique = dedupe(tech_raw)
    tech_ranked = rank_headlines(tech_unique, limit=15)
    for h in tech_ranked:
        h["title"] = rewrite_headline(h["title"])
    print(f"Tech: {len(tech_raw)} raw -> {len(tech_unique)} unique -> {len(tech_ranked)} selected")

    # Fetch portfolio news
    print("\n=== PORTFOLIO FEEDS ===")
    port_raw = _fetch_section(PORTFOLIO_FEEDS)
    port_unique = dedupe(port_raw)
    port_ranked = rank_headlines(port_unique, limit=15)
    for h in port_ranked:
        h["title"] = rewrite_headline(h["title"])
    print(
        f"Portfolio: {len(port_raw)} raw -> {len(port_unique)} unique -> {len(port_ranked)} selected"
    )

    # Fetch weather + market
    print("\n=== WEATHER ===")
    weather = fetch_weather()
    print("\n=== MARKET ===")
    dow = fetch_dow()
    if dow:
        sign = "+" if dow["change"] >= 0 else ""
        print(f"  [OK]   DJIA: {dow['price']:,.2f} ({sign}{dow['change']:,.2f})")

    # Build HTML
    html = build_page(news_ranked, tech_ranked, port_ranked, weather=weather, dow=dow)

    # Write output
    out_dir = Path(__file__).parent / "docs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"\nWrote {len(html)} bytes to {out_path}")


if __name__ == "__main__":
    main()
