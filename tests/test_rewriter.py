"""Tests for headline rewriting."""

from grudge.rewriter import rewrite_headline


def test_capitalizes_drama_words():
    result = rewrite_headline("Obama slams Trump on economy")
    assert "SLAMS" in result


def test_preserves_non_drama_words():
    result = rewrite_headline("Obama slams Trump on economy")
    assert "Obama" in result
    assert "Trump" in result
    assert "economy" in result


def test_max_caps_limit():
    title = "shocking scandal erupts as crisis collapses everything"
    result = rewrite_headline(title)
    caps_words = [w for w in result.split() if w.isupper() and len(w) > 2]
    assert len(caps_words) <= 3


def test_already_shouty_unchanged():
    title = "THIS IS ALREADY ALL CAPS NEWS"
    result = rewrite_headline(title)
    assert result == title


def test_no_drama_words_unchanged():
    title = "Local community holds bake sale"
    result = rewrite_headline(title)
    assert result == title


def test_word_boundary_respected():
    # "slams" should match but not partial words
    result = rewrite_headline("He slams the door")
    assert "SLAMS" in result
