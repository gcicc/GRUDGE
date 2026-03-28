"""Drama scoring and headline ranking."""

import re
from datetime import datetime, timezone

# Word → base points. Case-insensitive matching.
DRAMA_KEYWORDS: dict[str, int] = {
    "death": 5,
    "dead": 5,
    "dies": 5,
    "killed": 5,
    "war": 5,
    "invasion": 5,
    "explosion": 4,
    "crisis": 4,
    "bombshell": 4,
    "collapse": 4,
    "catastrophe": 4,
    "disaster": 4,
    "scandal": 3,
    "shock": 3,
    "shocking": 3,
    "erupts": 3,
    "fury": 3,
    "outrage": 3,
    "chaos": 3,
    "panic": 3,
    "urgent": 3,
    "slams": 2,
    "blasts": 2,
    "rips": 2,
    "warns": 2,
    "threat": 2,
    "exclusive": 2,
    "emergency": 2,
    "arrest": 2,
    "indicted": 3,
    "impeach": 4,
    "resign": 3,
    "fired": 2,
    "crash": 3,
    "surge": 2,
    "plunge": 3,
    "skyrocket": 2,
}

BREAKING_PATTERNS = [
    re.compile(r"^breaking\s*:", re.IGNORECASE),
    re.compile(r"^just\s+in\s*:", re.IGNORECASE),
    re.compile(r"^urgent\s*:", re.IGNORECASE),
]


def _keyword_score(title: str) -> float:
    """Sum drama points for keywords found in the title."""
    title_lower = title.lower()
    score = 0.0
    for word, points in DRAMA_KEYWORDS.items():
        if re.search(rf"\b{re.escape(word)}\b", title_lower):
            score += points
    return score


def _recency_multiplier(published: datetime) -> float:
    """Linear decay: 1.0 at 0h old, 0.0 at 24h old. Minimum 0.1 so old headlines aren't invisible."""
    now = datetime.now(timezone.utc)
    age_hours = (now - published).total_seconds() / 3600
    if age_hours < 0:
        age_hours = 0
    multiplier = max(0.1, 1.0 - (age_hours / 24.0))
    return multiplier


def is_breaking(title: str) -> bool:
    """Check if a headline is breaking news."""
    return any(p.search(title) for p in BREAKING_PATTERNS)


def score_headline(headline: dict) -> float:
    """Compute drama score for a single headline."""
    kw = _keyword_score(headline["title"])
    recency = _recency_multiplier(headline["published"])
    # Base score of 1 so every headline has some value
    base = max(kw, 1.0)
    score = base * recency
    # Breaking news bonus
    if is_breaking(headline["title"]):
        score *= 2.0
    return score


def rank_headlines(headlines: list[dict], limit: int = 25) -> list[dict]:
    """Score, sort, and return top headlines."""
    for h in headlines:
        h["score"] = score_headline(h)
        h["breaking"] = is_breaking(h["title"])
    headlines.sort(key=lambda h: h["score"], reverse=True)
    return headlines[:limit]
