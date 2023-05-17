#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from json import dumps
from pathlib import Path
from typing import List, Dict

from contexts.json_context import Json, JsonSafe, Single, SingleSafe
from scripts.files.export_file import text_export


def _convert_unknown(content: Single) -> SingleSafe:
    if isinstance(content, Path):
        return str(content)

    if isinstance(content, Decimal):
        return float(content)

    return content


def _serialize_json(content: Json) -> JsonSafe:
    if isinstance(content, Dict):
        return {key: _serialize_json(value) for key, value in content.items()}

    if isinstance(content, List):
        return [_serialize_json(value) for value in content]

    return _convert_unknown(content)


def json_dump(content: Json) -> str:
    return dumps(_serialize_json(content), indent=2, ensure_ascii=False, sort_keys=True)


def json_export(export_path: Path, content: Json) -> Path:
    return text_export(export_path, json_dump(content))
