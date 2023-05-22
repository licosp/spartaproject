#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

from contexts.json_context import Json, Single
from scripts.files.export_json import json_export
from scripts.files.import_json import json_load, json_import


def _common_test(input: Single, result: Json) -> None:
    if isinstance(result, Dict):
        assert input == result['group']


def _get_input_json(input: str) -> str:
    return '{"group": %s}' % input


def test_bool() -> None:
    input: bool = True
    _common_test(input, json_load(_get_input_json('true')))


def test_int() -> None:
    input: int = 1
    _common_test(input, json_load(_get_input_json(str(input))))


def test_float() -> None:
    input: float = 0.1
    _common_test(input, json_load(_get_input_json(str(input))))


def test_string() -> None:
    input: str = 'test'
    _common_test(input, json_load(_get_input_json('"%s"' % input)))


def test_export() -> None:
    INPUT: Json = [None, True, 1, 'test']

    with TemporaryDirectory() as tmp_path:
        json_path: Path = json_export(Path(tmp_path, 'tmp.ini'), INPUT)
        assert INPUT == json_import(json_path)


def main() -> bool:
    test_bool()
    test_int()
    test_float()
    test_string()
    test_export()
    return True
