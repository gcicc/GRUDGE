"""RSS feed fetching and normalization."""

from datetime import datetime, timezone

import feedparser

NEWS_FEEDS = [
    {"name": "Fox News", "url": "https://moxie.foxnews.com/google-publisher/latest.xml"},
    {"name": "NY Times", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
    {"name": "NY Post", "url": "https://nypost.com/feed/"},
    {"name": "Daily Mail", "url": "https://www.dailymail.co.uk/news/index.rss"},
    {"name": "BBC", "url": "https://feeds.bbci.co.uk/news/rss.xml"},
    {"name": "CNN", "url": "http://rss.cnn.com/rss/cnn_topstories.rss"},
    {"name": "Washington Post", "url": "https://feeds.washingtonpost.com/rss/national"},
    {"name": "Breitbart", "url": "https://feeds.feedburner.com/breitbart"},
    {"name": "The Hill", "url": "https://thehill.com/feed/"},
    {"name": "Politico", "url": "https://www.politico.com/rss/politicopicks.xml"},
]

TECH_FEEDS = [
    # AI company news & funding
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "The Information", "url": "https://www.theinformation.com/feed"},
    # AI research & tools
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml"},
    {"name": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/"},
    # Developer & startup ecosystem
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
    # Big tech moves & IPOs
    {"name": "Google News AI", "url": "https://news.google.com/rss/search?q=artificial+intelligence+company&hl=en-US&gl=US&ceid=US:en"},
]

# Tickers from E*Trade portfolios (IRA, Post-Tax, Roth)
PORTFOLIO_TICKERS = [
    # Core index/dividend ETFs
    "VOO", "VUG", "VIG", "VYM", "VO", "VXUS", "QQQM", "SCHD",
    # Sector
    "XLP",
    # Bonds
    "BND", "VTIP",
    # REITs
    "SCHH", "MITT", "TWO",
    # Income/covered call
    "QQQI",
    # Individual stocks
    "TSLA", "NVDA", "ISRG", "TSM", "UPS", "CPB",
    # Crypto/speculative
    "BITF", "EZBC", "QTUM",
    # Precious metals
    "GLDM", "SIVR", "IAU",
]

# Only fetch news for individual stocks and high-interest holdings (not broad ETFs)
PORTFOLIO_NEWS_TICKERS = ["TSLA", "NVDA", "ISRG", "TSM", "UPS", "CPB", "MITT", "TWO", "BITF"]

PORTFOLIO_FEEDS = [
    {"name": ticker, "url": f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"}
    for ticker in PORTFOLIO_NEWS_TICKERS
]

FEEDS = NEWS_FEEDS + TECH_FEEDS


def _parse_date(entry: dict) -> datetime:
    """Extract published date from feed entry, fallback to now."""
    for field in ("published_parsed", "updated_parsed"):
        parsed = entry.get(field)
        if parsed:
            try:
                from time import mktime

                return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
            except (ValueError, OverflowError, OSError):
                pass
    return datetime.now(timezone.utc)


def _normalize_entry(entry: dict, source: str) -> dict | None:
    """Convert a feedparser entry to a standard dict."""
    title = entry.get("title", "").strip()
    link = entry.get("link", "").strip()
    if not title or not link:
        return None
    return {
        "title": title,
        "link": link,
        "published": _parse_date(entry),
        "source": source,
    }


def fetch_feed(name: str, url: str, timeout: int = 10) -> list[dict]:
    """Fetch and normalize a single RSS feed."""
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "GRUDGE/0.1"})
        if feed.bozo and not feed.entries:
            print(f"  [SKIP] {name}: feed error")
            return []
        results = []
        for entry in feed.entries:
            normalized = _normalize_entry(entry, name)
            if normalized:
                results.append(normalized)
        print(f"  [OK]   {name}: {len(results)} headlines")
        return results
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return []


def fetch_all_feeds() -> list[dict]:
    """Fetch all configured feeds, return combined headline list."""
    print("Fetching feeds...")
    all_headlines = []
    for feed in FEEDS:
        all_headlines.extend(fetch_feed(feed["name"], feed["url"]))
    print(f"Total raw headlines: {len(all_headlines)}")
    return all_headlines
