#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from pathlib import Path

from scripts.bools.compare_dict import is_same_dict


def test_simple() -> None:
    assert is_same_dict({'A': True}, {'A': True})


def test_nest() -> None:
    assert is_same_dict({'A': {'B': True}}, {'A': {'B': True}})


def test_multi() -> None:
    assert is_same_dict({'A': True, 'B': False}, {'B': False, 'A': True})


def test_array() -> None:
    assert is_same_dict({'A': ['B', 'C']}, {'A': ['B', 'C']})


def test_type() -> None:
    assert is_same_dict(
        {
            'A': [None, True, 0, 0.1, 'test'],
            'B': [Decimal('-0.1'), Path('root')],
        },
        {
            'B': [Decimal('-0.1'), Path('root')],
            'A': [None, True, 0, 0.1, 'test'],
        },
    )


def main() -> bool:
    test_simple()
    test_nest()
    test_multi()
    test_array()
    test_type()
    return True
