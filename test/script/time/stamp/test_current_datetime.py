#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from pyspartaproj.context.default.integer_context import IntPair2
from pyspartaproj.script.time.format.create_iso_date import get_iso_time
from pyspartaproj.script.time.stamp.current_datetime import get_current_time


def _get_source() -> IntPair2:
    return {
        "year": {"year": 2023, "month": 4, "day": 1},
        "hour": {"hour": 0, "minute": 0, "second": 0},
        "zone": {"hour": 0, "minute": 0},
    }


def _get_source_jst() -> IntPair2:
    return {
        "year": {"year": 2023, "month": 4, "day": 1},
        "hour": {"hour": 9, "minute": 0, "second": 0},
        "zone": {"hour": 9, "minute": 0},
    }


def _common_test(time: datetime, expected: str) -> None:
    assert expected == time.isoformat()


def _compare_time(time: datetime, expected: IntPair2) -> None:
    assert get_iso_time(expected) == time


def test_utc() -> None:
    _compare_time(get_current_time(override=True), _get_source())


def test_jst() -> None:
    expected: str = "2023-04-01T09:00:00+09:00"
    _common_test(get_current_time(override=True, jst=True), expected)
