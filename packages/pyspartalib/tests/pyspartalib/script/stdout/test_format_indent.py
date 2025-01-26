#!/usr/bin/env python

"""Test module to remove white space at the beginning of a sentence."""

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.stdout.format_indent import format_indent


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _common_test(expected: Strs, source: str, stdout: bool = False) -> None:
    _difference_error(
        format_indent(source, stdout=stdout),
        "\n".join(expected),
    )


def test_stdout() -> None:
    """Test to remove white space at the beginning of a sentence."""
    source: str = """
        Hallo!
    """
    expected: Strs = ["Hallo!", ""]
    _common_test(expected, source, stdout=True)


def test_vertical() -> None:
    """Test to remove white space, tab character, and line break.

    Characters which should removed are placed to both ends of whole sentence.
    """
    source: str = """
    　\t
        Hallo!
    　\n
    """
    expected: Strs = ["Hallo!"]
    _common_test(expected, source)


def test_horizontal() -> None:
    """Test to remove white space, tab character, and line break.

    Characters which should removed are placed to both ends of one line text.
    """
    source: str = """
    \t　    Hallo!    　\n
    """
    expected: Strs = ["Hallo!"]
    _common_test(expected, source)


def test_indent() -> None:
    """Test to remove white space at the beginning of a sentence.

    Same count of white space are removed for all lines.
    """
    source: str = """
            Hallo!
        Hallo!
                Hallo!
    """
    expected: Strs = ["    Hallo!", "Hallo!", "        Hallo!"]
    _common_test(expected, source)


def test_inner() -> None:
    """Test to remove white space at the beginning of a sentence.

    Same count of white space are removed for all lines.
    But empty line is an exception.
    """
    source: str = """
        Hallo!    Hallo!


        Hallo!    Hallo!
    """
    expected: Strs = ["Hallo!    Hallo!", "", "", "Hallo!    Hallo!"]
    _common_test(expected, source)
