"""Tests for HTML generation."""

from datetime import datetime, timedelta, timezone

from grudge.html_builder import build_page


def _make_headlines(n: int = 10) -> list[dict]:
    return [
        {
            "title": f"Headline {i}",
            "link": f"https://example.com/{i}",
            "published": datetime.now(timezone.utc) - timedelta(hours=i),
            "source": "Test Source",
            "score": 10.0 - i,
            "breaking": i == 0,
        }
        for i in range(n)
    ]


def test_contains_times_new_roman():
    html = build_page(_make_headlines())
    assert "Times New Roman" in html


def test_contains_blue_links():
    html = build_page(_make_headlines())
    assert "color: blue" in html


def test_contains_grudge_title():
    html = build_page(_make_headlines())
    assert "GRUDGE REPORT" in html


def test_top_story_has_link():
    headlines = _make_headlines()
    html = build_page(headlines)
    assert headlines[0]["link"] in html


def test_all_headlines_present():
    headlines = _make_headlines(10)
    html = build_page(headlines)
    for h in headlines:
        assert h["title"] in html


def test_empty_headlines():
    html = build_page([])
    assert "NO HEADLINES AVAILABLE" in html


def test_breaking_emoji():
    headlines = _make_headlines(1)
    headlines[0]["breaking"] = True
    html = build_page(headlines)
    assert "\U0001f6a8" in html


def test_has_3_column_table():
    html = build_page(_make_headlines())
    assert "LEFT COLUMN" in html
    assert "CENTER COLUMN" in html
    assert "RIGHT COLUMN" in html


def test_tech_section_renders():
    tech = _make_headlines(3)
    html = build_page(_make_headlines(), tech=tech)
    assert "TECH &amp; AI" in html
    for h in tech:
        assert h["title"] in html


def test_no_tech_section_when_empty():
    html = build_page(_make_headlines(), tech=None)
    assert "TECH &amp; AI" not in html


def test_portfolio_section_renders():
    port = _make_headlines(3)
    html = build_page(_make_headlines(), portfolio=port)
    assert "MY PORTFOLIO" in html


def test_no_portfolio_when_empty():
    html = build_page(_make_headlines(), portfolio=None)
    assert "MY PORTFOLIO" not in html
