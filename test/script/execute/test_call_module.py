#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Call designated function of designated module."""

from pathlib import Path

from pytest import raises
from spartaproject.script.execute.call_module import call_function

_SOURCE_PATH: Path = Path(__file__)
_UNKNOWN: str = 'unknown'


def test_unknown_module() -> None:
    """Unknown function calling of designated module."""
    error_path = Path(_SOURCE_PATH).with_name(_UNKNOWN + '.py')
    with raises(FileNotFoundError):
        call_function(_SOURCE_PATH, error_path)


def test_unknown_function() -> None:
    """Main function calling of unknown module."""
    with raises(ModuleNotFoundError, match=_UNKNOWN):
        call_function(_SOURCE_PATH, _SOURCE_PATH, function=_UNKNOWN)


def test_pass() -> None:
    """Main function calling of designated module."""
    assert call_function(_SOURCE_PATH, _SOURCE_PATH)


def main() -> bool:
    """Test all public functions.

    Returns:
        bool: success if get to the end of function
    """
    test_pass()
    return True
