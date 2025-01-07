#!/usr/bin/env python

"""Test module to decode byte data by specific character encoding."""

from pyspartalib.script.string.encoding.set_decoding import set_decoding


def _compare_decoding(result: str) -> None:
    assert result == "\u3042"


def test_utf() -> None:
    """Test to decode byte data by default character encoding."""
    source: bytes = b"\xe3\x81\x82"

    _compare_decoding(set_decoding(source))


def test_sjis() -> None:
    """Test to decode byte data by specific character encoding."""
    source: bytes = b"\x82\xa0"

    _compare_decoding(set_decoding(source, encoding="shift_jis"))
