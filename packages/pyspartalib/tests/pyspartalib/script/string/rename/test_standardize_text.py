#!/usr/bin/env python

"""Test module to standardize string for key of dictionary."""

from pyspartalib.script.string.rename.standardize_text import StandardizeText


def _compare_text(expected: str, result: str) -> None:
    assert expected == result


def test_lower() -> None:
    """Test to convert upper case string to lower case."""
    _compare_text("test", StandardizeText().standardize("TEST", lower=True))


def test_all() -> None:
    """Test to convert string by using all conditions at once."""
    _compare_text(
        "name_domain_com",
        StandardizeText().standardize(
            " name@(domain).com ",
            lower=True,
            under=True,
            strip=True,
            replace=True,
        ),
    )
