#!/usr/bin/env python

"""Test module to export text file."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.extension.path_context import PathFunc
from pyspartalib.context.type_context import Type
from pyspartalib.script.file.text.export_file import byte_export, text_export
from pyspartalib.script.path.status.get_statistic import get_file_size


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _common_test(text_path: Path, count: int) -> None:
    _difference_error(get_file_size(text_path), count)


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        text_path: Path = Path(temporary_path, "temporary.txt")
        function(text_path)


def test_byte() -> None:
    """Test to export binary file."""
    source_byte: bytes = b"test"

    def individual_test(text_path: Path) -> None:
        _common_test(byte_export(text_path, source_byte), len(source_byte))

    _inside_temporary_directory(individual_test)


def test_text() -> None:
    """Test to export text file."""
    source_text: str = "test"

    def individual_test(text_path: Path) -> None:
        _common_test(text_export(text_path, source_text), len(source_text))

    _inside_temporary_directory(individual_test)
