#!/usr/bin/env python

"""Test module to export data used for json format."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.file.json_context import Json
from pyspartalib.context.type_context import Type
from pyspartalib.script.file.json.export_json import json_dump, json_export
from pyspartalib.script.file.text.import_file import text_import
from pyspartalib.script.string.format_texts import format_indent


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _common_test(expected: str, source: Json) -> None:
    _difference_error(json_dump(source), format_indent(expected))


def test_type() -> None:
    """Test to convert data used for json format to text.

    Data is a dictionary created with multiple mixed type.
    """
    source: Json = {
        "None": None,
        "bool": True,
        "int": 1,
        "float": 1.0,
        "str": "1",
    }

    # 2 space indent
    expected: str = """
      {
        "None": null,
        "bool": true,
        "float": 1.0,
        "int": 1,
        "str": "1"
      }
    """

    _common_test(expected, source)


def test_tree() -> None:
    """Test to convert data used for json format to text.

    Data is multiple dimensional dictionary created with None object.
    """
    source: Json = {"0": {"1": {"2": {"3": {"4": {"5": {"6": None}}}}}}}
    expected: str = """
    {
      "0": {
        "1": {
          "2": {
            "3": {
              "4": {
                "5": {
                  "6": null
                }
              }
            }
          }
        }
      }
    }
    """

    _common_test(expected, source)


def test_compress() -> None:
    """Test to convert data used for json format with compress option."""
    source: Json = {"0": {"1": {"2": {"3": {"4": {"5": {"6": None}}}}}}}
    expected: str = """{"0":{"1":{"2":{"3":{"4":{"5":{"6":null}}}}}}}"""

    _difference_error(json_dump(source, compress=True), expected)


def test_export() -> None:
    """Test to export data used for json format."""
    keys: Json = ["R", "G", "B"]
    expected: str = """
      [
        "R",
        "G",
        "B"
      ]
    """

    with TemporaryDirectory() as temporary_path:
        _difference_error(
            text_import(
                json_export(Path(temporary_path, "temporary.json"), keys),
            ),
            format_indent(expected),
        )
