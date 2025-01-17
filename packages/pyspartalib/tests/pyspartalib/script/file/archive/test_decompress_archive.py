#!/usr/bin/env python

"""Test module to decompress file or directory by archive format."""

from base64 import b64decode
from collections.abc import Sized
from datetime import datetime
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.default.integer_context import IntPair2, Ints2
from pyspartalib.context.default.string_context import StrPair, Strs
from pyspartalib.context.extension.path_context import PathFunc, Paths, Paths2
from pyspartalib.context.extension.time_context import Times, Times2
from pyspartalib.context.type_context import Type
from pyspartalib.script.directory.create_parent import create_parent
from pyspartalib.script.file.archive.compress_archive import CompressArchive
from pyspartalib.script.file.archive.decompress_archive import (
    DecompressArchive,
)
from pyspartalib.script.file.json.convert_to_json import multiple_to_json
from pyspartalib.script.file.json.export_json import json_export
from pyspartalib.script.file.text.export_file import byte_export
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.path.modify.current.get_relative import (
    get_relative_array,
)
from pyspartalib.script.path.safe.safe_trash import SafeTrash
from pyspartalib.script.path.status.get_statistic import get_file_size_array
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from pyspartalib.script.stdout.format_indent import format_indent
from pyspartalib.script.time.format.create_iso_date import get_iso_time
from pyspartalib.script.time.path.get_timestamp import get_latest
from pyspartalib.script.time.path.set_timestamp import set_latest


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _length_error(result: Sized, expected: int) -> None:
    if len(result) == expected:
        raise ValueError


def _success_error(status: bool) -> None:
    if status:
        raise ValueError


def _get_multiple() -> str:
    return "\u3042"


def _get_types() -> Strs:
    return ["tree", "extract"]


def _get_source() -> IntPair2:
    return {
        "year": {"year": 2023, "month": 4, "day": 15},
        "hour": {"hour": 20, "minute": 9, "second": 30, "micro": 936886},
        "zone": {"hour": 0, "minute": 0},
    }


def _get_tree_root(temporary_root: Path) -> Path:
    return Path(temporary_root, "tree")


def _get_extract_root(temporary_root: Path) -> Path:
    return Path(temporary_root, "extract")


def _get_archive_root(temporary_root: Path) -> Path:
    return Path(temporary_root, "archive")


def _get_multiple_data() -> StrPair:
    return {"multiple": _get_multiple()}


def _get_multiple_element() -> Strs:
    multiple: str = _get_multiple()
    return [multiple, multiple + ".json"]


def _get_multiple_path(tree_root: Path) -> Path:
    return Path(tree_root, *_get_multiple_element())


def _export_multiple(config_path: Path, config_data: StrPair) -> None:
    create_parent(config_path)
    json_export(config_path, multiple_to_json(config_data))


def _export_byte(file_path: Path, byte: bytes) -> Path:
    create_parent(file_path)
    return byte_export(file_path, byte)


def _get_expected_stamp() -> datetime:
    return get_iso_time(_get_source())


def _get_times_pair(sorted_paths: Paths2) -> Times2:
    return [
        [get_latest(path) for path in paths if path.is_file()]
        for paths in sorted_paths
    ]


def _get_times(times_pair: Times2) -> Times:
    return list(set(chain(*times_pair)))


def _compare_timestamp(sorted_paths: Paths2, expected: datetime) -> None:
    times_pair: Times2 = _get_times_pair(sorted_paths)
    _difference_error(*times_pair)

    times: Times = _get_times(times_pair)
    _length_error(times, 1)
    _difference_error(times[0], expected)


def _compare_path_pair(left: Paths, right: Paths) -> None:
    _length_error({str(sorted(paths)) for paths in [left, right]}, 1)


def _get_relative_paths(sorted_paths: Paths2, temporary_root: Path) -> Paths2:
    return [
        get_relative_array(paths, root_path=Path(temporary_root, directory))
        for directory, paths in zip(_get_types(), sorted_paths, strict=True)
    ]


def _compare_path_name(sorted_paths: Paths2, temporary_root: Path) -> None:
    _difference_error(*_get_relative_paths(sorted_paths, temporary_root))


def _get_file_size_pair(sorted_paths: Paths2) -> Ints2:
    return [get_file_size_array(paths) for paths in sorted_paths]


def _compare_file_size(sorted_paths: Paths2) -> None:
    _difference_error(*_get_file_size_pair(sorted_paths))


def _get_sorted_path(walk_root: Path) -> Paths:
    return sorted(walk_iterator(walk_root))


def _get_sorted_paths(temporary_root: Path) -> Paths2:
    return [
        _get_sorted_path(Path(temporary_root, directory))
        for directory in _get_types()
    ]


def _common_test(temporary_root: Path) -> Paths2:
    sorted_paths: Paths2 = _get_sorted_paths(temporary_root)

    _compare_path_name(sorted_paths, temporary_root)
    _compare_file_size(sorted_paths)

    return sorted_paths


def _type_test(temporary_root: Path, same_type: bool) -> None:
    _common_test(temporary_root)
    _success_error(same_type)


def _sequential_test(
    temporary_root: Path,
    archive_paths: Paths,
    sequential: Paths,
) -> None:
    _common_test(temporary_root)
    _compare_path_pair(archive_paths, sequential)


def _timestamp_test(temporary_root: Path) -> None:
    _compare_timestamp(_common_test(temporary_root), _get_expected_stamp())


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def _set_file_latest(paths: Paths) -> None:
    latest: datetime = _get_expected_stamp()
    for path in paths:
        if path.is_file():
            set_latest(path, latest)


def _filter_length(result: Sized, expected: int) -> bool:
    return len(result) == expected


def _find_unused(paths: Paths) -> Paths:
    return [
        path
        for path in paths
        if _filter_length(list(walk_iterator(path, depth=1)), 0)
    ]


def _remove_unused(paths: Paths) -> None:
    SafeTrash().trash_at_once(paths)


def _create_tree(temporary_root: Path) -> Path:
    return create_temporary_tree(_get_tree_root(temporary_root))


def _create_tree_file(temporary_root: Path) -> Path:
    return create_temporary_tree(_get_tree_root(temporary_root), tree_deep=2)


def _create_tree_directory(temporary_root: Path) -> Path:
    return create_temporary_tree(_get_tree_root(temporary_root), tree_deep=3)


def _create_tree_sequential(temporary_root: Path) -> Path:
    return create_temporary_tree(_get_tree_root(temporary_root), tree_deep=5)


def _get_tree_paths(path: Path) -> Paths:
    return list(walk_iterator(path))


def _get_tree_paths_file(path: Path) -> Paths:
    return list(walk_iterator(path, file=False))


def _get_tree_paths_directory(path: Path) -> Paths:
    return list(walk_iterator(path, directory=False))


def _compress_archive(temporary_root: Path) -> CompressArchive:
    return CompressArchive(_get_archive_root(temporary_root))


def _compress_archive_sequential(temporary_root: Path) -> CompressArchive:
    return CompressArchive(_get_archive_root(temporary_root), limit_byte=200)


def _decompress_archive(temporary_root: Path) -> DecompressArchive:
    return DecompressArchive(_get_extract_root(temporary_root))


def _compress_at_once(
    tree_path: Path,
    paths: Paths,
    compress_archive: CompressArchive,
) -> None:
    compress_archive.compress_at_once(paths, archive_root=tree_path)


def _from_compress_single(
    temporary_root: Path,
    tree_path: Path,
    add_paths: Paths,
) -> CompressArchive:
    compress_archive: CompressArchive = _compress_archive(temporary_root)
    _compress_at_once(tree_path, add_paths, compress_archive)
    return compress_archive


def _from_compress_sequential(
    temporary_root: Path,
    tree_path: Path,
    add_paths: Paths,
) -> CompressArchive:
    compress_archive: CompressArchive = _compress_archive_sequential(
        temporary_root,
    )
    _compress_at_once(tree_path, add_paths, compress_archive)
    return compress_archive


def _decompress_single(
    archive_paths: Paths,
    decompress_archive: DecompressArchive,
) -> None:
    decompress_archive.decompress_archive(archive_paths[0])


def _decompress_type(
    archive_paths: Paths,
    decompress_archive: DecompressArchive,
) -> bool:
    return decompress_archive.is_lzma_archive(archive_paths[0])


def _decompress_sequential(
    archive_paths: Paths,
    decompress_archive: DecompressArchive,
) -> Paths:
    sequential: Paths = decompress_archive.sequential_archives(
        archive_paths[0],
    )
    decompress_archive.decompress_at_once(sequential)
    return sequential


def _to_decompress_single(
    temporary_root: Path,
    archive_paths: Paths,
) -> DecompressArchive:
    decompress_archive: DecompressArchive = _decompress_archive(temporary_root)
    _decompress_single(archive_paths, decompress_archive)
    return decompress_archive


def _finalize_compress_single(
    temporary_root: Path,
    tree_path: Path,
    add_paths: Paths,
) -> Paths:
    compress_archive: CompressArchive = _from_compress_single(
        temporary_root,
        tree_path,
        add_paths,
    )
    return compress_archive.close_archived()


def _finalize_compress_sequential(
    temporary_root: Path,
    tree_path: Path,
    add_paths: Paths,
) -> Paths:
    compress_archive: CompressArchive = _from_compress_sequential(
        temporary_root,
        tree_path,
        add_paths,
    )
    return compress_archive.close_archived()


def _compress_to_decompress(
    temporary_root: Path,
    tree_path: Path,
    add_paths: Paths,
) -> None:
    _to_decompress_single(
        temporary_root,
        _finalize_compress_single(temporary_root, tree_path, add_paths),
    )


def _remove_unused_file(tree_path: Path) -> None:
    _remove_unused(_find_unused(_get_tree_paths_file(tree_path)))


def _remove_unused_directory(tree_path: Path) -> None:
    _remove_unused(_get_tree_paths_directory(tree_path))


def _get_archive_string() -> str:
    return """
        UEsDBBQAAAAAAA0XKlkAAAAAAAAAAAAAAAALAAAAYXJjaGl2ZS
        +CoC9QSwMEFAAAAAAA/RYqWa89DlEVAAAAFQAAABIAAABhcmNo
        aXZlL4KgL4KgLmpzb257DQogICAgImtleSI6IuOBgiINCn1QSw
        ECFAAUAAAAAAANFypZAAAAAAAAAAAAAAAACwAAAAAAAAAAABAA
        AAAAAAAAYXJjaGl2ZS+CoC9QSwECFAAUAAAAAAD9FipZrz0OUR
        UAAAAVAAAAEgAAAAAAAAABACAAAAApAAAAYXJjaGl2ZS+CoC+C
        oC5qc29uUEsFBgAAAAACAAIAeQAAAG4AAAAAAA==
    """


def _get_archive_byte() -> bytes:
    return b64decode(
        "".join(format_indent(_get_archive_string()).splitlines()),
    )


def _get_result_archive(temporary_root: Path) -> Paths:
    extract_root: Path = _get_extract_root(temporary_root)

    return get_relative_array(
        _get_sorted_path(extract_root),
        root_path=extract_root,
    )


def _get_expected_paths(path_names: Strs) -> Paths:
    return [
        Path(*[path_names[j] for j in range(i + 1)])
        for i in range(len(path_names))
    ]


def _get_expected_archive() -> Paths:
    return _get_expected_paths(["archive", *_get_multiple_element()])


def _archive_test(temporary_root: Path) -> None:
    _difference_error(
        _get_result_archive(temporary_root),
        _get_expected_archive(),
    )


def _export_byte_archive(temporary_root: Path) -> Path:
    return _export_byte(
        Path(_get_archive_root(temporary_root), "archive.zip"),
        _get_archive_byte(),
    )


def test_file() -> None:
    """Test to decompress archive including only files."""

    def individual_test(temporary_root: Path) -> None:
        tree_path: Path = _create_tree_file(temporary_root)

        _remove_unused_file(tree_path)
        _compress_to_decompress(
            temporary_root,
            tree_path,
            _get_tree_paths(tree_path),
        )

        _common_test(temporary_root)

    _inside_temporary_directory(individual_test)


def test_directory() -> None:
    """Test to decompress archive including only directories."""

    def individual_test(temporary_root: Path) -> None:
        tree_path: Path = _create_tree_directory(temporary_root)

        _remove_unused_directory(tree_path)
        _compress_to_decompress(
            temporary_root,
            tree_path,
            _get_tree_paths(tree_path),
        )

        _common_test(temporary_root)

    _inside_temporary_directory(individual_test)


def test_type() -> None:
    """Test to get type of compression format from archive."""

    def individual_test(temporary_root: Path) -> None:
        tree_path: Path = _create_tree(temporary_root)

        archive_paths: Paths = _finalize_compress_single(
            temporary_root,
            tree_path,
            _get_tree_paths(tree_path),
        )
        same_type: bool = _decompress_type(
            archive_paths,
            _to_decompress_single(temporary_root, archive_paths),
        )

        _type_test(temporary_root, same_type)

    _inside_temporary_directory(individual_test)


def test_sequential() -> None:
    """Test to decompress sequential archives."""

    def individual_test(temporary_root: Path) -> None:
        tree_path: Path = _create_tree_sequential(temporary_root)

        archive_paths: Paths = _finalize_compress_sequential(
            temporary_root,
            tree_path,
            _get_tree_paths(tree_path),
        )
        sequential: Paths = _decompress_sequential(
            archive_paths,
            _decompress_archive(temporary_root),
        )

        _sequential_test(temporary_root, archive_paths, sequential)

    _inside_temporary_directory(individual_test)


def test_timestamp() -> None:
    """Test for timestamp consistency of contents in archive."""

    def individual_test(temporary_root: Path) -> None:
        tree_path: Path = _create_tree(temporary_root)

        add_paths: Paths = _get_tree_paths(tree_path)
        _set_file_latest(add_paths)
        _compress_to_decompress(temporary_root, tree_path, add_paths)

        _timestamp_test(temporary_root)

    _inside_temporary_directory(individual_test)


def test_multiple() -> None:
    """Test to decompress archive including multiple byte character."""

    def individual_test(temporary_root: Path) -> None:
        tree_root: Path = _get_tree_root(temporary_root)
        _export_multiple(_get_multiple_path(tree_root), _get_multiple_data())

        _compress_to_decompress(
            temporary_root,
            tree_root,
            _get_tree_paths(tree_root),
        )

        _common_test(temporary_root)

    _inside_temporary_directory(individual_test)


def test_archive() -> None:
    """Test to decompress archive encoded by shift-jis group."""

    def individual_test(temporary_root: Path) -> None:
        _to_decompress_single(
            temporary_root,
            [_export_byte_archive(temporary_root)],
        )

        _archive_test(temporary_root)

    _inside_temporary_directory(individual_test)
