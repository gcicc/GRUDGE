"""Tests for drama scoring."""

from datetime import datetime, timedelta, timezone

from grudge.scorer import is_breaking, rank_headlines, score_headline


def _make_headline(title: str, hours_ago: float = 0.5) -> dict:
    return {
        "title": title,
        "link": "https://example.com",
        "published": datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        "source": "Test Source",
    }


def test_keyword_score_high():
    h = _make_headline("DEATH toll rises in WAR zone")
    score = score_headline(h)
    assert score > 5.0


def test_keyword_score_boring():
    h = _make_headline("Local park opens new playground")
    score = score_headline(h)
    assert score < 2.0


def test_recency_matters():
    fresh = _make_headline("Crisis erupts downtown", hours_ago=0.1)
    stale = _make_headline("Crisis erupts downtown", hours_ago=20.0)
    assert score_headline(fresh) > score_headline(stale)


def test_breaking_detection():
    assert is_breaking("BREAKING: Major event")
    assert is_breaking("Just In: Something happened")
    assert not is_breaking("This is regular news")


def test_breaking_bonus():
    normal = _make_headline("Crisis in the capital")
    breaking = _make_headline("BREAKING: Crisis in the capital")
    assert score_headline(breaking) > score_headline(normal)


def test_rank_limits():
    headlines = [_make_headline(f"Headline {i}") for i in range(50)]
    ranked = rank_headlines(headlines, limit=10)
    assert len(ranked) == 10


def test_rank_order():
    high = _make_headline("DEATH and DISASTER strike nation")
    low = _make_headline("Nice weather expected tomorrow")
    ranked = rank_headlines([low, high], limit=2)
    assert ranked[0]["title"] == high["title"]
