#!/usr/bin/env python

"""Test module to confirm that type bool values are same and True."""

from pyspartalib.context.default.bool_context import BoolPair, Bools
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.bool.same_value import bool_same_array, bool_same_pair


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _success_error(status: bool) -> None:
    if status:
        raise ValueError


def _expected_list(status: bool) -> Bools:
    return [status] * 3


def _expected_keys() -> Strs:
    return ["R", "G", "B"]


def _expected_pair(status: bool) -> BoolPair:
    return dict(zip(_expected_keys(), _expected_list(status), strict=True))


def test_empty() -> None:
    """Test for list of bool value as empty."""
    _success_error(bool_same_array([]))


def test_mixed() -> None:
    """Test for list of bool value which is mix of True and False."""
    _success_error(bool_same_array([False, True, False]))


def test_false() -> None:
    """Test for list of bool value which is all False."""
    _success_error(bool_same_array(_expected_list(False)))


def test_array() -> None:
    """Test for list of bool value which is all True."""
    _fail_error(bool_same_array(_expected_list(True)))


def test_invert() -> None:
    """Test for list of bool value with invert option."""
    _fail_error(bool_same_array(_expected_list(False), invert=True))


def test_pair() -> None:
    """Test for pair of bool value which is all True."""
    _fail_error(bool_same_pair(_expected_pair(True)))


def test_pair_invert() -> None:
    """Test for pair of bool value with invert option."""
    _fail_error(bool_same_pair(_expected_pair(False), invert=True))
