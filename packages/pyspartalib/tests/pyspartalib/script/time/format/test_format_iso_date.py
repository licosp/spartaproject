#!/usr/bin/env python

"""Test module to convert date time element to several types."""

from pyspartalib.context.default.integer_context import IntPair, IntPair2, Ints
from pyspartalib.context.default.string_context import StrPair, StrPair2, Strs
from pyspartalib.context.file.json_context import Jsons
from pyspartalib.script.bool.compare_json import is_same_json
from pyspartalib.script.file.json.convert_to_json import multiple2_to_json
from pyspartalib.script.time.format.format_iso_date import format_iso_date


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_source_year() -> IntPair:
    return {"year": 2023, "month": 4, "day": 1}


def _get_source_error_year() -> IntPair:
    return {"year": 2023, "error": 123}


def _get_source_hour() -> IntPair:
    return {"hour": 4, "minute": 51, "second": 30, "micro": 123}


def _get_source_zone() -> IntPair:
    return {"hour": 9, "minute": 15}


def _get_source_all() -> IntPair2:
    return {
        "year": _get_source_year(),
        "hour": _get_source_hour(),
        "zone": _get_source_zone(),
    }


def _get_source_error() -> IntPair2:
    return {
        "year": _get_source_error_year(),
        "error": {"hour": 4, "error": 456},
    }


def _format_digit(number: int, digit: int) -> str:
    return str(number).zfill(digit)


def _format_digit_type(source: IntPair, groups: Strs, digits: Ints) -> StrPair:
    return {
        group: _format_digit(source[group], digit)
        for group, digit in zip(groups, digits, strict=True)
    }


def _get_expected_year() -> StrPair:
    return _format_digit_type(
        _get_source_year(),
        ["year", "month", "day"],
        [4] + [2] * 2,
    )


def _get_expected_error_year() -> StrPair:
    return _format_digit_type(_get_source_error_year(), ["year"], [4])


def _get_expected_hour() -> StrPair:
    return _format_digit_type(
        _get_source_hour(),
        ["hour", "minute", "second", "micro"],
        [2] * 3 + [6],
    )


def _get_expected_zone() -> StrPair:
    return _format_digit_type(_get_source_zone(), ["hour", "minute"], [2] * 2)


def _get_expected_all() -> StrPair2:
    return {
        "year": _get_expected_year(),
        "hour": _get_expected_hour(),
        "zone": _get_expected_zone(),
    }


def _get_expected_error() -> StrPair2:
    return {"year": _get_expected_error_year()}


def _convert_to_json(left: StrPair2, right: StrPair2) -> Jsons:
    return [multiple2_to_json(date) for date in [left, right]]


def _compare_datetime(source: IntPair2, expected: StrPair2) -> None:
    _fail_error(
        is_same_json(*_convert_to_json(format_iso_date(source), expected)),
    )


def test_all() -> None:
    """Compare date time element structured by type string."""
    _compare_datetime(_get_source_all(), _get_expected_all())


def test_error() -> None:
    """Compare date time element which is error data."""
    _compare_datetime(_get_source_error(), _get_expected_error())
