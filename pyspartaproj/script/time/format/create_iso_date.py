#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

from pyspartaproj.context.default.integer_context import IntPair2
from pyspartaproj.context.default.string_context import (
    StrPair,
    StrPair2,
    Strs,
    Strs2,
)
from pyspartaproj.script.time.format.format_iso_date import format_iso_date


def _get_groups() -> Strs:
    return ["year", "hour", "zone"]


def _get_types_year() -> Strs:
    return ["year", "month", "day"]


def _get_types_hour() -> Strs:
    return ["hour", "minute", "second"]


def _get_types_zone() -> Strs:
    return ["hour", "minute"]


def _get_types() -> Strs2:
    return [_get_types_year(), _get_types_hour(), _get_types_zone()]


def _get_type_identifiers() -> Strs:
    return ["-"] + [":"] * 2


def _get_group_identifiers() -> Strs:
    return ["T", "+", ""]


def _get_group_string(
    identifier: str, key_types: Strs, iso_group: StrPair
) -> str:
    return identifier.join([iso_group[key_type] for key_type in key_types])


def _get_group_strings(string_elements: StrPair2) -> StrPair:
    return {
        group: _get_group_string(identifier, key_types, string_elements[group])
        for group, key_types, identifier in zip(
            _get_groups(), _get_types(), _get_type_identifiers()
        )
        if group in string_elements
    }


def _get_microsecond(iso_date: StrPair2) -> str | None:
    if "hour" in iso_date:
        hour_date = iso_date["hour"]

        if "micro" in hour_date:
            return hour_date["micro"]

    return None


def _add_microsecond(
    string_elements: StrPair2, group_strings: StrPair
) -> None:
    if millisecond := _get_microsecond(string_elements):
        group_strings["hour"] += "." + millisecond


def _get_datetime_elements(group_strings: StrPair) -> Strs:
    iso_strings: Strs = []

    for group, identifier in zip(_get_groups(), _get_group_identifiers()):
        if group in group_strings:
            iso_strings += [group_strings[group], identifier]

    return iso_strings[:-1]


def _merge_datetime_elements(group_strings: StrPair) -> str:
    return "".join(_get_datetime_elements(group_strings))


def get_iso_string(iso_date: IntPair2) -> str:
    string_elements: StrPair2 = format_iso_date(iso_date)
    group_strings: StrPair = _get_group_strings(string_elements)
    _add_microsecond(string_elements, group_strings)

    return _merge_datetime_elements(group_strings)


def get_iso_time(iso_date: IntPair2) -> datetime:
    return datetime.fromisoformat(get_iso_string(iso_date))


def get_iso_epoch(iso_date: IntPair2) -> Decimal:
    return Decimal(str(get_iso_time(iso_date).timestamp()))
