"""Tests for headline de-duplication."""

from datetime import datetime, timezone

from run import _dedupe_key, dedupe


def _h(title: str) -> dict:
    return {
        "title": title,
        "link": "https://example.com",
        "published": datetime.now(timezone.utc),
        "source": "Test",
    }


def test_exact_duplicates_removed():
    out = dedupe([_h("Big News Today"), _h("Big News Today")])
    assert len(out) == 1


def test_case_and_punctuation_insensitive():
    out = dedupe([_h("Markets CRASH!"), _h("markets crash")])
    assert len(out) == 1


def test_publisher_suffix_ignored():
    # Same story syndicated by two outlets (Google News style suffix)
    out = dedupe([_h("Tornado hits town - CNN"), _h("Tornado hits town - Fox News")])
    assert len(out) == 1


def test_distinct_headlines_kept():
    out = dedupe([_h("Story A"), _h("Story B")])
    assert len(out) == 2


def test_shared_seen_set_across_sections():
    seen: set[str] = set()
    news = dedupe([_h("Shared Story")], seen)
    tech = dedupe([_h("Shared Story")], seen)
    assert len(news) == 1
    assert len(tech) == 0


def test_dedupe_key_strips_punctuation():
    assert _dedupe_key("Hello, World!") == _dedupe_key("hello world")
