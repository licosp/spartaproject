#!/usr/bin/env python

"""Test module to standardize string for key of dictionary."""

from pyspartalib.context.type_context import Type
from pyspartalib.script.string.rename.standardize_text import StandardizeText


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def test_lower() -> None:
    """Test to convert upper case string to lower case."""
    _difference_error(
        StandardizeText().standardize("TEST", lower=True),
        "test",
    )


def test_all() -> None:
    """Test to convert string by using all conditions at once."""
    _difference_error(
        StandardizeText().standardize(
            " name@(domain).com ",
            lower=True,
            under=True,
            strip=True,
            replace=True,
        ),
        "name_domain_com",
    )
