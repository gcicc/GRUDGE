"""Tests for market timestamp handling."""

from datetime import datetime, timezone

from grudge.market import epoch_to_et


def test_epoch_to_et_winter_is_est():
    # 2026-01-15 21:00 UTC = 16:00 EST
    ts = epoch_to_et(datetime(2026, 1, 15, 21, 0, tzinfo=timezone.utc).timestamp())
    assert ts.strftime("%I:%M %p") == "04:00 PM"
    assert ts.utcoffset().total_seconds() == -5 * 3600


def test_epoch_to_et_summer_is_edt():
    # 2026-07-15 20:00 UTC = 16:00 EDT
    ts = epoch_to_et(datetime(2026, 7, 15, 20, 0, tzinfo=timezone.utc).timestamp())
    assert ts.strftime("%I:%M %p") == "04:00 PM"
    assert ts.utcoffset().total_seconds() == -4 * 3600
