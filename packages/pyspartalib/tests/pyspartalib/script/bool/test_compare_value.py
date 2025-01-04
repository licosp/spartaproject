#!/usr/bin/env python

from pyspartalib.script.bool.compare_value import (
    bool_compare_array,
    bool_compare_pair,
)
from tests.pyspartalib.interface.pytest import raises


def test_size() -> None:
    with raises(ValueError, match="size"):
        bool_compare_array([True], [True, False])


def test_empty() -> None:
    with raises(ValueError, match="empty"):
        bool_compare_array([], [])


def test_key() -> None:
    with raises(KeyError, match="unmatch"):
        bool_compare_pair(
            {"R": False, "G": True, "B": True},
            {"R": True, "error": False, "B": True},
        )


def test_array() -> None:
    if not bool_compare_array([True, False], [True, False]):
        raise ValueError


def test_pair() -> None:
    if not bool_compare_pair(
        {"R": True, "G": False, "B": True},
        {"R": True, "G": False, "B": True},
    ):
        raise ValueError
