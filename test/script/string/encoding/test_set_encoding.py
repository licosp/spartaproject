#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test module to encode string by specific character encoding."""

from pyspartaproj.script.string.encoding.set_encoding import set_encoding


def _compare_encoding(expected: bytes, result: bytes) -> None:
    assert expected == result


def _test_character() -> str:
    return "\u3042"


def test_utf() -> None:
    """Test to encode string by default character encoding."""
    expected: bytes = b"\xe3\x81\x82"

    _compare_encoding(expected, set_encoding(_test_character()))


def test_sjis() -> None:
    """Test to encode string by specific character encoding."""
    expected: bytes = b"\x82\xa0"

    _compare_encoding(
        expected, set_encoding(_test_character(), encoding="shift_jis")
    )
