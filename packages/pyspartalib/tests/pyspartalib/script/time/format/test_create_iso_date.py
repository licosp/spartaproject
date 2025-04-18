#!/usr/bin/env python

"""Test module to convert date time element to several types."""

from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.integer_context import IntPair, IntPair2
from pyspartalib.script.time.format.create_iso_date import (
    get_iso_epoch,
    get_iso_string,
    get_iso_time,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_years() -> IntPair:
    return {"year": 2023, "month": 4, "day": 1}


def _get_hours() -> IntPair:
    return {"hour": 4, "minute": 51, "second": 30, "micro": 123}


def _get_zones() -> IntPair:
    return {"hour": 9, "minute": 0}


def _get_source_all() -> IntPair2:
    return {"year": _get_years(), "hour": _get_hours(), "zone": _get_zones()}


def _get_source_micro() -> IntPair2:
    return {
        "year": _get_years(),
        "hour": {"hour": 4, "minute": 51, "second": 30},
        "zone": _get_zones(),
    }


def _set_expected_time(
    year: IntPair,
    hour: IntPair,
    tzinfo: ZoneInfo,
) -> datetime:
    return datetime(
        year["year"],
        year["month"],
        year["day"],
        hour["hour"],
        hour["minute"],
        hour["second"],
        hour["micro"],
        tzinfo=tzinfo,
    )


def _get_expected_time(source: IntPair2) -> datetime:
    return _set_expected_time(
        source["year"],
        source["hour"],
        ZoneInfo("Asia/Tokyo"),
    )


def _get_expected_epoch() -> Decimal:
    return Decimal("1680292290.000123")


def _get_source_zone() -> IntPair2:
    return {"year": _get_years(), "hour": _get_hours()}


def _get_expected_all() -> str:
    return "2023-04-01T04:51:30.000123+09:00"


def _get_expected_micro() -> str:
    return "2023-04-01T04:51:30+09:00"


def _get_expected_zone() -> str:
    return "2023-04-01T04:51:30.000123"


def _compare_string(source: IntPair2, expected: str) -> None:
    _difference_error(get_iso_string(source), expected)


def _compare_time(source: IntPair2, expected: datetime) -> None:
    _difference_error(get_iso_time(source), expected)


def _compare_epoch(source: IntPair2, expected: Decimal) -> None:
    _difference_error(get_iso_epoch(source), expected)


def test_all() -> None:
    """Test to compare date time strings of ISO date format."""
    _compare_string(_get_source_all(), _get_expected_all())


def test_micro() -> None:
    """Test to compare date time strings without microsecond value."""
    _compare_string(_get_source_micro(), _get_expected_micro())


def test_zone() -> None:
    """Test to compare date time strings without time zone value."""
    _compare_string(_get_source_zone(), _get_expected_zone())


def test_time() -> None:
    """Test to compare date time objects."""
    source: IntPair2 = _get_source_all()
    _compare_time(source, _get_expected_time(source))


def test_epoch() -> None:
    """Test to compare date time value of UNIX epoch."""
    _compare_epoch(_get_source_all(), _get_expected_epoch())
