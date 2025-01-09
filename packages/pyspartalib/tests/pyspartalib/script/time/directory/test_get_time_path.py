#!/usr/bin/env python

"""Test module to get constant value including time information."""

from pathlib import Path

from pyspartalib.context.type_context import Type
from pyspartalib.script.time.directory.get_time_path import (
    get_initial_time_path,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_hour(jst: bool) -> str:
    return str(9 if jst else 0).zfill(2)


def _get_time_path(jst: bool = False) -> Path:
    return Path("2023", "04", "01", _get_hour(jst), "00", "00", "000000")


def test_utc() -> None:
    """Test to get path represent April 1, 2023 as UTC time zone."""
    _difference_error(get_initial_time_path(), _get_time_path())


def test_jst() -> None:
    """Test to get path represent April 1, 2023 as JST time zone."""
    _difference_error(
        get_initial_time_path(jst=True),
        _get_time_path(jst=True),
    )
