#!/usr/bin/env python

"""Test module to convert time data from epoch format to datetime object."""

from datetime import datetime
from decimal import Decimal

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.integer_context import IntPair2
from pyspartalib.script.time.epoch.from_timestamp import time_from_timestamp
from pyspartalib.script.time.format.create_iso_date import (
    get_iso_epoch,
    get_iso_time,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_source() -> IntPair2:
    return {
        "year": {"year": 2023, "month": 4, "day": 15},
        "hour": {"hour": 20, "minute": 9, "second": 30, "micro": 936886},
        "zone": {"hour": 0, "minute": 0},
    }


def _get_source_jst() -> IntPair2:
    return {
        "year": {"year": 2023, "month": 4, "day": 16},
        "hour": {"hour": 5, "minute": 9, "second": 30, "micro": 936886},
        "zone": {"hour": 9, "minute": 0},
    }


def _get_iso_time() -> datetime:
    return get_iso_time(_get_source())


def _get_iso_time_jst() -> datetime:
    return get_iso_time(_get_source_jst())


def _get_iso_epoch() -> Decimal:
    return get_iso_epoch(_get_source())


def test_utc() -> None:
    """Test to convert time data from epoch format to datetime object."""
    _difference_error(time_from_timestamp(_get_iso_epoch()), _get_iso_time())


def test_jst() -> None:
    """Test to convert time data to datetime object as JST time zone."""
    _difference_error(
        time_from_timestamp(_get_iso_epoch(), jst=True),
        _get_iso_time_jst(),
    )
