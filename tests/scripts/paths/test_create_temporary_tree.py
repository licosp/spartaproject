#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
from typing import Callable

from contexts.integer_context import Ints
from contexts.path_context import Path, Paths
from contexts.string_context import Strs, Strs2
from scripts.paths.create_temporary_tree import create_tree
from scripts.paths.get_relative import get_relative_array
from scripts.paths.iterate_directory import walk_iterator


def _inside_tmp_directory(function: Callable[[Path], None]) -> Paths:
    with TemporaryDirectory() as tmp_path:
        root_path: Path = Path(tmp_path)
        function(root_path)
        return get_relative_array(
            list(walk_iterator(root_path)), root_path=root_path
        )


def test_three() -> None:
    NAME_DIR_1: str = 'dir001'
    NAME_DIR_2: str = 'dir002'
    NAME_DIRS: Strs = [NAME_DIR_1, NAME_DIR_2]
    NAME_DIR_EMPTY: str = 'empty'

    NAME_INI: str = 'file.ini'
    NAME_JSON: str = 'file.json'
    NAME_TEXT: str = 'file.txt'

    EXPECTED: Strs2 = [
        [NAME_DIR_1],
        [NAME_DIR_EMPTY],
        [NAME_INI],
        [NAME_JSON],
        [NAME_TEXT],
        NAME_DIRS,
        [NAME_DIR_1, NAME_DIR_EMPTY],
        [NAME_DIR_1, NAME_INI],
        [NAME_DIR_1, NAME_JSON],
        [NAME_DIR_1, NAME_TEXT],
        NAME_DIRS + [NAME_DIR_EMPTY],
        NAME_DIRS + [NAME_INI],
        NAME_DIRS + [NAME_JSON],
        NAME_DIRS + [NAME_TEXT],
    ]

    expected: Paths = [Path(*path_names) for path_names in EXPECTED]

    def individual_test(tmp_path: Path) -> None:
        create_tree(tmp_path, tree_deep=3)

    assert expected == _inside_tmp_directory(individual_test)


def test_deep() -> None:
    OUTRANGE_INDICES: Ints = [-1, 0, 11, 12, 13]

    def individual_test(tmp_path: Path) -> None:
        for index in OUTRANGE_INDICES:
            create_tree(tmp_path, tree_deep=index)

    assert 0 == len(_inside_tmp_directory(individual_test))


def test_weight() -> None:
    OUTRANGE_INDICES: Ints = [-2, -1, 0, 11, 12, 13]

    def individual_test(tmp_path: Path) -> None:
        for index in OUTRANGE_INDICES:
            create_tree(tmp_path, tree_weight=index)

    assert 0 == len(_inside_tmp_directory(individual_test))


def main() -> bool:
    test_three()
    test_deep()
    test_weight()
    return True
