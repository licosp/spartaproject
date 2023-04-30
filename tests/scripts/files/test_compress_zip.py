#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shutil import unpack_archive
from typing import Callable
from tempfile import TemporaryDirectory

from contexts.integer_context import Ints, Ints2
from contexts.path_context import Path, Paths, Paths2
from scripts.files.compress_zip import ArchiveZip
from scripts.paths.get_relative import path_array_relative
from scripts.paths.create_tmp_tree import create_tree
from scripts.paths.iterate_directory import walk_iterator


def _get_input_paths(walk_paths: Paths, tmp_path: Path) -> Paths:
    inputs: Paths = []
    tree_root: Path = Path(tmp_path, 'tree')

    for walk_path in walk_paths:
        inputs += [walk_path]
        parent_path: Path = walk_path.parent

        if tree_root != parent_path:
            inputs += [parent_path]

        if walk_path.is_dir():
            for path in walk_iterator(walk_path):
                inputs += [path]

    return inputs


def _get_output_paths(result_raw: Paths, tmp_path: Path) -> Paths:
    outputs: Paths = []
    extract_root: Path = Path(tmp_path, 'extract')

    for result_path in result_raw:
        unpack_archive(result_path, extract_dir=extract_root)

        for path in walk_iterator(extract_root):
            outputs += [path]

    return outputs


def _compare_path_count(sorted_paths: Paths2) -> None:
    counts: Ints = [len(paths) for paths in sorted_paths]
    assert counts[0] == counts[1]


def _compare_path_name(sorted_paths: Paths2, tmp_path: Path) -> None:
    relative_paths: Paths2 = [
        path_array_relative(paths, root_path=Path(tmp_path, directory))
        for directory, paths in zip(['tree', 'extract'], sorted_paths)
    ]

    assert relative_paths[0] == relative_paths[1]


def _compare_file_size(sorted_paths: Paths2) -> None:
    file_size_pair: Ints2 = [
        [path.stat().st_size for path in paths if path.is_file()]
        for paths in sorted_paths
    ]

    assert file_size_pair[0] == file_size_pair[1]


def _get_sorted_paths(walk_paths: Paths, result_raw: Paths, tmp_path: Path) -> Paths2:
    inputs: Paths = _get_input_paths(walk_paths, tmp_path)
    outputs: Paths = _get_output_paths(result_raw, tmp_path)

    return [
        sorted(list(set(paths)))
        for paths in [inputs, outputs]
    ]


def _check_archive_result(
    result_raw: Paths,
    tmp_path: Path,
    walk_paths: Paths,
) -> Paths2:
    sorted_paths: Paths2 = _get_sorted_paths(walk_paths, result_raw, tmp_path)

    _compare_path_count(sorted_paths)
    _compare_path_name(sorted_paths, tmp_path)
    _compare_file_size(sorted_paths)

    return sorted_paths


def _inside_tmp_directory(func: Callable[[Path], None]) -> None:
    with TemporaryDirectory() as tmp_path:
        func(Path(tmp_path))


def test_simple() -> None:
    def make_tree(tmp_path: Path) -> None:
        tree_root: Path = Path(tmp_path, 'tree')
        archive_zip = ArchiveZip(Path(tmp_path, 'archive'))
        create_tree(tree_root)

        walk_paths: Paths = []
        for path in walk_iterator(tree_root, directory=False, depth=1):
            archive_zip.add_archive(path)
            walk_paths += [path]

        result_raw: Paths = archive_zip.result()
        del archive_zip
        _check_archive_result(result_raw, tmp_path, walk_paths)

    _inside_tmp_directory(make_tree)


def test_directory() -> None:
    def make_tree(tmp_path: Path) -> None:
        tree_root: Path = Path(tmp_path, 'tree')
        archive_zip = ArchiveZip(Path(tmp_path, 'archive'))
        create_tree(tree_root, tree_deep=2)

        walk_paths: Paths = []
        for path in walk_iterator(tree_root, file=False, depth=1):
            archive_zip.add_archive(path)
            walk_paths += [path]

        result_raw: Paths = archive_zip.result()
        del archive_zip
        _check_archive_result(result_raw, tmp_path, walk_paths)

    _inside_tmp_directory(make_tree)


def test_tree() -> None:
    def make_tree(tmp_path: Path) -> None:
        tree_root: Path = Path(tmp_path, 'tree')
        archive_zip = ArchiveZip(Path(tmp_path, 'archive'))
        create_tree(tree_root, tree_deep=3)

        walk_paths: Paths = []
        for path in walk_iterator(tree_root, directory=False, suffix='txt'):
            archive_zip.add_archive(path, archive_root=tree_root)
            walk_paths += [path]

        result_raw: Paths = archive_zip.result()
        del archive_zip
        _check_archive_result(result_raw, tmp_path, walk_paths)

    _inside_tmp_directory(make_tree)


def main() -> bool:
    test_simple()
    test_directory()
    test_tree()
    return True
