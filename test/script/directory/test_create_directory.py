#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test module to create empty directory or directories."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

from pyspartaproj.context.default.string_context import Strs
from pyspartaproj.context.extension.path_context import PathPair, Paths
from pyspartaproj.script.bool.same_value import bool_same_array, bool_same_pair
from pyspartaproj.script.directory.create_directory import (
    create_directory,
    create_directory_array,
    create_directory_pair,
)
from pyspartaproj.script.path.modify.get_absolute import get_absolute_array
from pyspartaproj.script.path.status.check_exists import (
    check_exists_array,
    check_exists_pair,
)


def _get_element_names() -> Strs:
    return ["R", "G", "B"]


def _get_head_path(index: int) -> Path:
    element_names: Strs = _get_element_names()
    return Path(*[element_names[i] for i in range(index + 1)])


def _inside_temporary_directory(function: Callable[[Path], bool]) -> None:
    with TemporaryDirectory() as temporary_path:
        assert function(Path(temporary_path))


def test_single() -> None:
    """Test to create empty directory to the path you specified."""
    element_names: Strs = _get_element_names()

    def individual_test(temporary_path: Path) -> bool:
        path: Path = create_directory(Path(temporary_path, element_names[0]))
        return path.exists()

    _inside_temporary_directory(individual_test)


def _get_directory_array(temporary_root: Path, paths: Paths) -> Paths:
    return create_directory_array(
        get_absolute_array(paths, root_path=temporary_root)
    )


def _get_directory_pair(
    temporary_path: Path, head_paths: PathPair
) -> PathPair:
    paths: PathPair = {
        name: Path(temporary_path, head_path)
        for name, head_path in head_paths.items()
    }
    return create_directory_pair(create_directory_pair(paths))


def test_array() -> None:
    """Test to create empty directories which is specified by list."""
    head_paths: Paths = [
        _get_head_path(i) for i, _ in enumerate(_get_element_names())
    ]

    def individual_test(temporary_path: Path) -> bool:
        return bool_same_array(
            check_exists_array(
                _get_directory_array(temporary_path, head_paths)
            )
        )

    _inside_temporary_directory(individual_test)


def test_pair() -> None:
    """Test to create empty directories which is specified by dictionary."""
    head_paths: PathPair = {
        name: _get_head_path(i) for i, name in enumerate(_get_element_names())
    }

    def individual_test(temporary_path: Path) -> bool:
        return bool_same_pair(
            check_exists_pair(_get_directory_pair(temporary_path, head_paths))
        )

    _inside_temporary_directory(individual_test)


def main() -> bool:
    """Run all tests.

    Returns:
        bool: Success if get to the end of function.
    """
    test_single()
    test_array()
    test_pair()
    return True
