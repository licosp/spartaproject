#! /usr/bin/env python

"""Test module to get path in local resource directory."""

from pathlib import Path

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.file.json.convert_from_json import (
    string_pair_from_json,
)
from pyspartalib.script.file.json.import_json import json_import
from pyspartalib.script.path.modify.get_resource import get_resource


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _common_test(expected: str, path_elements: Strs) -> None:
    result_path: Path = get_resource(local_path=Path(*path_elements))

    _difference_error(
        string_pair_from_json(json_import(result_path))["name"],
        expected,
    )


def test_file() -> None:
    """Test to get path in local resource file."""
    expected: str = "file"
    _common_test(expected, [expected + ".json"])


def test_directory() -> None:
    """Test to get path in local resource directory and file."""
    expected: str = "directory"
    _common_test(expected, [expected, "file.json"])
