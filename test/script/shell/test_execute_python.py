#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test to execute Python corresponding to platform."""

from pathlib import Path
from platform import uname

from pyspartaproj.context.default.string_context import Strs
from pyspartaproj.context.extension.path_context import Paths
from pyspartaproj.script.path.modify.get_absolute import get_absolute
from pyspartaproj.script.path.modify.get_relative import get_relative
from pyspartaproj.script.path.modify.get_resource import get_resource
from pyspartaproj.script.shell.execute_python import (
    execute_python,
    get_script_string,
)
from pyspartaproj.script.string.temporary_text import temporary_text


def _get_script_text(script_text: str) -> str:
    return get_script_string(get_resource(local_path=Path(script_text)))


def _get_system_paths(expected: Paths, first_root: Path) -> Paths:
    system_paths: Paths = []

    for result in execute_python(
        [_get_script_text("local_import.py")], python_paths=expected
    ):
        path: Path = Path(result)

        if path.is_relative_to(get_absolute(first_root)):
            system_paths += [get_relative(path)]

    return system_paths


def _compare_system_paths(expected: Paths, results: Paths) -> None:
    assert 1 == len(set([str(sorted(paths)) for paths in [expected, results]]))


def test_path() -> None:
    """Test to convert path to the format for executing script in Python."""
    path_elements: Strs = ["A", "B", "C"]
    identifier: str = "/" if "Linux" == uname().system else "\\"

    assert identifier.join(path_elements) == get_script_string(
        Path(*path_elements)
    )


def test_command() -> None:
    """Test to execute simple Python script."""
    assert temporary_text(3, 3) == list(
        execute_python([_get_script_text("indices.py")])
    )


def test_platform() -> None:
    """Test to execute Python script for all executable platform."""
    expected: Strs = ["linux", "windows"]

    assert expected == [
        result.lower()
        for platform in expected
        for result in execute_python(
            [_get_script_text("execute_platform.py")],
            platform=platform,
        )
    ]


def main() -> bool:
    """Run all tests.

    Returns:
        bool: Success if get to the end of function.
    """
    test_path()
    test_command()
    test_platform()
    return True
