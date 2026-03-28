"""Headline rewriting with strategic ALL CAPS."""

import re

# Words to capitalize for maximum drama
CAPS_WORDS: set[str] = {
    "slams",
    "rips",
    "blasts",
    "destroys",
    "erupts",
    "explodes",
    "crashes",
    "collapses",
    "warns",
    "threatens",
    "demands",
    "fires",
    "shocking",
    "stunning",
    "exclusive",
    "bombshell",
    "outrage",
    "fury",
    "chaos",
    "panic",
    "crisis",
    "scandal",
    "disaster",
    "catastrophe",
    "surge",
    "plunge",
    "skyrocket",
    "dead",
    "killed",
    "exposed",
    "busted",
    "caught",
    "revealed",
    "secretly",
    "massive",
    "urgent",
}

MAX_CAPS_PER_HEADLINE = 3


def _already_shouty(title: str) -> bool:
    """Check if headline is already mostly caps."""
    alpha = [c for c in title if c.isalpha()]
    if not alpha:
        return False
    caps_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
    return caps_ratio > 0.5


def rewrite_headline(title: str) -> str:
    """Apply strategic ALL CAPS to drama words in a headline."""
    if _already_shouty(title):
        return title

    caps_applied = 0

    def _caps_replacer(match: re.Match) -> str:
        nonlocal caps_applied
        if caps_applied >= MAX_CAPS_PER_HEADLINE:
            return match.group(0)
        caps_applied += 1
        return match.group(0).upper()

    # Build pattern matching any caps word at word boundaries
    pattern = r"\b(" + "|".join(re.escape(w) for w in CAPS_WORDS) + r")\b"
    result = re.sub(pattern, _caps_replacer, title, flags=re.IGNORECASE)
    return result
