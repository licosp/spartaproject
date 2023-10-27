#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from platform import uname

from pyspartaproj.context.default.string_context import Strs
from pyspartaproj.script.path.modify.get_resource import get_resource
from pyspartaproj.script.shell.execute_powershell import (
    execute_powershell,
    get_path_string,
    get_quoted_path,
    get_script_executable,
    get_script_string,
)


def _get_shortcut_command(shortcut_path: Path) -> str:
    return get_script_executable(
        [
            get_script_string(get_resource(Path("read.ps1"))),
            get_quoted_path(get_path_string(shortcut_path)),
        ]
    )


def _execute_script(shortcut_path: Path) -> Strs:
    return list(execute_powershell([_get_shortcut_command(shortcut_path)]))


def _check_shortcut_exists(shortcut_path: Path) -> None:
    if not shortcut_path.exists():
        raise FileNotFoundError()


def _remove_drive_head(path_text: str) -> Path:
    if "Linux" == uname().system:
        if "C:" == path_text[:2]:
            path: Path = Path(path_text[2:].replace("\\", "/"))

            if path.exists():
                return path

    return Path(path_text)


def read_shortcut(shortcut_path: Path) -> Path | None:
    _check_shortcut_exists(shortcut_path)

    result: Strs = _execute_script(shortcut_path)

    if 1 == len(result):
        return _remove_drive_head(result[0])

    return None
