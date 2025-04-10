#!/usr/bin/env python

"""Test module to confirm that characters in selected string.

Each character should be included in user defined character tables.
"""

from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.string.table.filter_table import FilterTable


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _success_error(status: bool) -> None:
    if status:
        raise ValueError


def _filter_text(texts: Strs, filter_table: FilterTable) -> bool:
    return filter_table.contain("".join(texts))


def _enable_text(texts: Strs, filter_table: FilterTable) -> None:
    _fail_error(_filter_text(texts, filter_table))


def _disable_text(texts: Strs, filter_table: FilterTable) -> None:
    _success_error(_filter_text(texts, filter_table))


def _get_zero(multiple: bool = False) -> str:
    return "\uff10" if multiple else "0"


def test_ascii() -> None:
    """Test to confirm that characters in Ascii table are included."""
    _enable_text(["A", "a", _get_zero()], FilterTable())


def test_other() -> None:
    """Test to confirm that characters not in Ascii table are included."""
    _disable_text(["À", "à", _get_zero()], FilterTable())


def test_multiple() -> None:
    """Test to confirm that multiple byte characters are included."""
    _enable_text(
        ["\uff21", "\uff41", _get_zero(multiple=True)],
        FilterTable(multiple=True),
    )


def test_jp() -> None:
    """Test to confirm that Japanese characters are included."""
    _disable_text(
        ["\u3042", "\u3044", _get_zero(multiple=True)],
        FilterTable(multiple=True),
    )
