#!/usr/bin/env python

"""Test module to convert multiple byte characters.

There are converted to single byte same characters in Ascii table.
"""

from pyspartalib.context.type_context import Type
from pyspartalib.script.string.rename.convert_single import ConvertSingle


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _common_test(expected: str, text: str) -> None:
    _difference_error(ConvertSingle().convert(text), expected)


def test_error() -> None:
    """Test to convert unsupported character."""
    text: str = "\u3042"
    expected: str = text

    _common_test(expected, text)


def test_single() -> None:
    """Test to convert upper case letter."""
    text: str = "\uff21"
    expected: str = "A"

    _common_test(expected, text)


def test_array() -> None:
    """Test to convert list of multiple byte character."""
    text: str = "\uff34\uff25\uff33\uff34"
    expected: str = "TEST"

    _common_test(expected, text)


def test_small() -> None:
    """Test to convert lower case letter."""
    text: str = "\uff41"
    expected: str = "a"

    _common_test(expected, text)


def test_number() -> None:
    """Test to convert number character."""
    text: str = "\uff10"
    expected: str = "0"

    _common_test(expected, text)


def test_other() -> None:
    """Test to convert character other than alphabet and number."""
    text: str = "\uff5e"
    expected: str = "~"

    _common_test(expected, text)
