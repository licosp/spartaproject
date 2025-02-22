#!/usr/bin/env python

"""Test module to edit internal of archive file."""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.extension.path_context import (
    PathFunc,
    PathPair,
    Paths,
    Paths2,
)
from pyspartalib.context.extension.time_context import TimePair
from pyspartalib.script.directory.create_directory import create_directory
from pyspartalib.script.file.archive.compress_archive import CompressArchive
from pyspartalib.script.file.archive.decompress_archive import (
    DecompressArchive,
)
from pyspartalib.script.file.archive.edit_archive import EditArchive
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.path.modify.current.get_relative import (
    get_relative,
    is_relative,
)
from pyspartalib.script.path.safe.safe_rename import SafeRename
from pyspartalib.script.path.safe.safe_trash import SafeTrash
from pyspartalib.script.path.status.get_statistic import get_file_size
from pyspartalib.script.path.temporary.create_temporary_file import (
    create_temporary_file,
)
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from pyspartalib.script.time.directory.get_time_path import (
    get_initial_time_path,
)
from pyspartalib.script.time.path.get_timestamp import (
    get_directory_latest,
    get_invalid_time,
)
from pyspartalib.script.time.stamp.is_same_stamp import is_same_stamp


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _none_error(result: Type | None) -> Type:
    if result is None:
        raise ValueError

    return result


def _not_none_error(result: object) -> None:
    if result is not None:
        raise ValueError


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _success_error(status: bool) -> None:
    if status:
        raise ValueError


def _no_exists_error(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError


def _get_name() -> str:
    return "temporary"


def _get_root_before(temporary_root: Path) -> Path:
    return Path(temporary_root, "before")


def _get_root_after(temporary_root: Path) -> Path:
    return Path(temporary_root, "after")


def _get_root_archive(temporary_root: Path) -> Path:
    return Path(temporary_root, "archive")


def _get_root_edit(temporary_root: Path) -> Path:
    return Path(temporary_root, "edit")


def _add_archive(
    temporary_root: Path,
    compress_archive: CompressArchive,
) -> Paths:
    compress_archive.compress_at_once(
        list(walk_iterator(_get_root_before(temporary_root))),
    )

    return compress_archive.close_archived()


def _get_stamp_key(path_text: str, stamp_root: Path) -> str:
    return str(get_relative(Path(path_text), root_path=stamp_root))


def _get_stamp_value(path_text: str, time: datetime) -> datetime:
    return get_invalid_time() if Path(path_text).is_dir() else time


def _get_archive_stamp(stamp_root: Path) -> TimePair:
    latest_times: TimePair = get_directory_latest(walk_iterator(stamp_root))
    return {
        _get_stamp_key(key, stamp_root): _get_stamp_value(key, time)
        for key, time in latest_times.items()
    }


def _get_archive_stamp_before(temporary_root: Path) -> TimePair:
    return _get_archive_stamp(_get_root_before(temporary_root))


def _get_archive_stamp_after(temporary_root: Path) -> TimePair:
    return _get_archive_stamp(_get_root_after(temporary_root))


def _create_source(temporary_root: Path) -> None:
    create_temporary_tree(_get_root_before(temporary_root))


def _create_source_compress(temporary_root: Path) -> None:
    create_temporary_tree(_get_root_before(temporary_root), tree_weight=3)


def _initialize_archive(temporary_root: Path) -> TimePair:
    _create_source(temporary_root)
    return _get_archive_stamp_before(temporary_root)


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def _add_to_archived(archive_root: Path) -> Path:
    return create_temporary_file(archive_root)


def _remove_from_archived(archive_root: Path) -> Path:
    return SafeTrash().trash(Path(archive_root, "file.txt"))


def _update_to_archived(archive_root: Path) -> Path:
    rename_path: Path = Path(archive_root, "file.ini")

    safe_rename = SafeRename()
    safe_rename.rename(rename_path, rename_path.with_name("rename"))

    return rename_path


def _edit_to_archived(archive_root: Path) -> PathPair:
    edit_history: PathPair = {
        "add": _add_to_archived(archive_root),
        "remove": _remove_from_archived(archive_root),
        "update": _update_to_archived(archive_root),
    }

    return {
        key: get_relative(path, root_path=archive_root)
        for key, path in edit_history.items()
    }


def _decompress_archive(after_root: Path, archive_paths: Paths) -> None:
    DecompressArchive(after_root).decompress_at_once(archive_paths)


def _remove_stamp_after(path_text: str, stamp_after: TimePair) -> None:
    del stamp_after[path_text]


def _remove_time_stamp(edit_history: PathPair, stamp_after: TimePair) -> None:
    _remove_stamp_after(str(edit_history["add"]), stamp_after)


def _add_stamp_after(
    edit_type: str,
    edit_history: PathPair,
    stamp_before: TimePair,
    stamp_after: TimePair,
) -> None:
    path_text: str = str(edit_history[edit_type])
    stamp_after[path_text] = stamp_before[path_text]


def _add_time_stamp(
    edit_history: PathPair,
    stamp_before: TimePair,
    stamp_after: TimePair,
) -> None:
    _add_stamp_after("remove", edit_history, stamp_before, stamp_after)


def _update_time_stamp(
    edit_history: PathPair,
    stamp_before: TimePair,
    stamp_after: TimePair,
) -> None:
    _remove_stamp_after("rename", stamp_after)
    _add_stamp_after("update", edit_history, stamp_before, stamp_after)


def _edit_time_stamp(
    edit_history: PathPair,
    stamp_before: TimePair,
    stamp_after: TimePair,
) -> None:
    _remove_time_stamp(edit_history, stamp_after)
    _add_time_stamp(edit_history, stamp_before, stamp_after)
    _update_time_stamp(edit_history, stamp_before, stamp_after)


def _get_decompress_stamp(
    temporary_root: Path,
    archive_paths: Paths,
) -> TimePair:
    _decompress_archive(_get_root_after(temporary_root), archive_paths)
    return _get_archive_stamp_after(temporary_root)


def _get_stamp_after(
    temporary_root: Path,
    stamp_before: TimePair,
    edit_history: PathPair,
    archive_paths: Paths,
) -> TimePair:
    stamp_after: TimePair = _get_decompress_stamp(
        temporary_root,
        archive_paths,
    )
    _edit_time_stamp(edit_history, stamp_before, stamp_after)

    return stamp_after


def _find_decompress_root(temporary_root: Path, remove_root: Path) -> TimePair:
    return _get_decompress_stamp(
        temporary_root,
        list(walk_iterator(remove_root, directory=False)),
    )


def _get_edit_history(edit_archive: EditArchive) -> PathPair:
    return _edit_to_archived(edit_archive.get_edit_root())


def _compare_path(result: Path, expected: Path) -> None:
    _no_exists_error(result)
    _difference_error(result, expected)


def _compare_root(trash_root: Path, edit_archive: EditArchive) -> None:
    _compare_path(
        edit_archive.get_edit_root(),
        Path(trash_root, get_initial_time_path()),
    )


def _close_archive(edit_archive: EditArchive) -> Paths:
    return _none_error(edit_archive.close_archive())


def _close_archive_fail(edit_archive: EditArchive) -> None:
    _not_none_error(edit_archive.close_archive())


def _stamp_test(stamp_before: TimePair, stamp_after: TimePair) -> None:
    _fail_error(is_same_stamp(stamp_before, stamp_after))


def _compare_not_relative(full_path: Path, root_path: Path) -> None:
    _success_error(is_relative(full_path, root_path=root_path))


def _open_test(archive_path: Path, edit_archive: EditArchive) -> None:
    _difference_error(
        edit_archive.open_archive(archive_path=archive_path),
        archive_path,
    )


def _common_test(
    temporary_root: Path,
    stamp_before: TimePair,
    edit_archive: EditArchive,
) -> None:
    _stamp_test(
        stamp_before,
        _get_stamp_after(
            temporary_root,
            stamp_before,
            _get_edit_history(edit_archive),
            _close_archive(edit_archive),
        ),
    )


def _protect_test(
    temporary_root: Path,
    stamp_before: TimePair,
    edit_archive: EditArchive,
) -> None:
    _get_edit_history(edit_archive)
    _close_archive_fail(edit_archive)

    _stamp_test(
        stamp_before,
        _find_decompress_root(
            temporary_root,
            _get_root_archive(temporary_root),
        ),
    )


def _remove_test(
    temporary_root: Path,
    stamp_before: TimePair,
    edit_archive: EditArchive,
) -> None:
    _get_edit_history(edit_archive)
    _close_archive(edit_archive)

    _stamp_test(
        stamp_before,
        _find_decompress_root(temporary_root, edit_archive.get_trash_root()),
    )


def _get_sorted_paths(before_paths: Paths, after_paths: Paths) -> Paths2:
    return [sorted(paths) for paths in [before_paths, after_paths]]


def _name_test(before_path: Path, edit_archive: EditArchive) -> None:
    _get_edit_history(edit_archive)

    _difference_error(_close_archive(edit_archive)[0], before_path)
    _difference_error(_get_name(), before_path.stem)


def _path_test(archive_path: Path, edit_archive: EditArchive) -> None:
    _difference_error(edit_archive.get_archive_path(), archive_path)


def _limit_test(before_paths: Paths, edit_archive: EditArchive) -> None:
    _get_edit_history(edit_archive)
    after_paths: Paths = _close_archive(edit_archive)

    _difference_error(*_get_sorted_paths(before_paths, after_paths))


def _compress_test(archive_path: Path, edit_archive: EditArchive) -> None:
    archive_size_before: int = get_file_size(archive_path)
    _close_archive(edit_archive)
    _fail_error(archive_size_before > get_file_size(archive_path))


def _get_archive(temporary_root: Path) -> CompressArchive:
    return CompressArchive(_get_root_archive(temporary_root))


def _get_archive_name(temporary_root: Path) -> CompressArchive:
    return CompressArchive(
        _get_root_archive(temporary_root),
        archive_id=_get_name(),
    )


def _get_archive_limit(
    temporary_root: Path,
    limit_byte: int,
) -> CompressArchive:
    return CompressArchive(
        _get_root_archive(temporary_root),
        limit_byte=limit_byte,
    )


def _get_archive_path(temporary_root: Path) -> Path:
    return _add_archive(temporary_root, _get_archive(temporary_root))[0]


def _get_archive_path_name(temporary_root: Path) -> Paths:
    return _add_archive(temporary_root, _get_archive_name(temporary_root))


def _get_archive_path_limit(temporary_root: Path, limit_byte: int) -> Paths:
    return _add_archive(
        temporary_root,
        _get_archive_limit(temporary_root, limit_byte),
    )


def _get_edit() -> EditArchive:
    return EditArchive()


def _get_edit_work(working_root: Path) -> EditArchive:
    return EditArchive(working_root=working_root, override=True)


def _get_edit_edit(working_root: Path) -> EditArchive:
    return EditArchive(edit_root=working_root, override=True)


def _get_edit_path(archive_path: Path) -> EditArchive:
    edit_archive: EditArchive = _get_edit()
    edit_archive.open_archive(archive_path=archive_path)
    return edit_archive


def _get_edit_limit(archive_path: Path, limit_byte: int) -> EditArchive:
    edit_archive: EditArchive = _get_edit()
    edit_archive.open_archive(archive_path=archive_path, limit_byte=limit_byte)
    return edit_archive


def _get_edit_compress(archive_path: Path) -> EditArchive:
    edit_archive: EditArchive = _get_edit()
    edit_archive.open_archive(archive_path=archive_path, compress=True)
    return edit_archive


def _get_edit_protect(archive_path: Path) -> EditArchive:
    edit_archive: EditArchive = _get_edit()
    edit_archive.open_archive(archive_path=archive_path, protected=True)
    return edit_archive


def _get_edit_remove(archive_path: Path, remove_root: Path) -> EditArchive:
    edit_archive = EditArchive(trash_root=remove_root)
    edit_archive.open_archive(archive_path=archive_path)
    return edit_archive


def test_error() -> None:
    """Test to confirm that path of archive is undefined."""
    edit_archive: EditArchive = _get_edit()

    with pytest.raises(ValueError):
        edit_archive.get_archive_path()


def test_disable() -> None:
    """Test to confirm path of archive is undefined."""
    _fail_error(_get_edit().is_disable_archive())


def test_none() -> None:
    """Test to open archive with out archive path."""
    _not_none_error(_get_edit().open_archive())


def test_close() -> None:
    """Test to close archive with out archive path."""
    _close_archive_fail(_get_edit())


def test_work() -> None:
    """Test to compare user defined temporary working space."""

    def individual_test(temporary_root: Path) -> None:
        _compare_root(temporary_root, _get_edit_work(temporary_root))

    _inside_temporary_directory(individual_test)


def test_different() -> None:
    """Test to compare 2 type of temporary working spaces."""

    def individual_test(temporary_root: Path) -> None:
        edit_archive: EditArchive = _get_edit_edit(temporary_root)

        _compare_not_relative(
            edit_archive.get_edit_root(),
            edit_archive.get_working_root(),
        )

    _inside_temporary_directory(individual_test)


def test_edit() -> None:
    """Test to get temporary working spaces to edit archive."""

    def individual_test(temporary_root: Path) -> None:
        edit_root: Path = _get_root_edit(temporary_root)
        _compare_root(edit_root, _get_edit_edit(edit_root))

    _inside_temporary_directory(individual_test)


def test_single() -> None:
    """Test to compare internal of single archive file."""

    def individual_test(temporary_root: Path) -> None:
        _common_test(
            temporary_root,
            _initialize_archive(temporary_root),
            _get_edit_path(_get_archive_path(temporary_root)),
        )

    _inside_temporary_directory(individual_test)


def test_open() -> None:
    """Test to open archive with archive path successfully."""

    def individual_test(temporary_root: Path) -> None:
        _create_source(temporary_root)

        _open_test(_get_archive_path(temporary_root), _get_edit())

    _inside_temporary_directory(individual_test)


def test_name() -> None:
    """Test to compare name of archive before edit and after."""

    def individual_test(temporary_root: Path) -> None:
        _create_source(temporary_root)
        archive_path: Path = _get_archive_path_name(temporary_root)[0]

        _name_test(archive_path, _get_edit_path(archive_path))

    _inside_temporary_directory(individual_test)


def test_path() -> None:
    """Test to compare path of archive."""

    def individual_test(temporary_root: Path) -> None:
        _create_source(temporary_root)
        archive_path: Path = _get_archive_path(temporary_root)

        _path_test(archive_path, _get_edit_path(archive_path))

    _inside_temporary_directory(individual_test)


def test_limit() -> None:
    """Test to compare archive paths before edit and after."""
    limit_byte: int = 100

    def individual_test(temporary_root: Path) -> None:
        _create_source(temporary_root)
        archive_paths: Paths = _get_archive_path_limit(
            temporary_root,
            limit_byte,
        )

        _limit_test(
            archive_paths,
            _get_edit_limit(archive_paths[0], limit_byte),
        )

    _inside_temporary_directory(individual_test)


def test_compress() -> None:
    """Test to compare size of archive files."""

    def individual_test(temporary_root: Path) -> None:
        _create_source_compress(temporary_root)
        archive_path: Path = _get_archive_path(temporary_root)

        _compress_test(archive_path, _get_edit_compress(archive_path))

    _inside_temporary_directory(individual_test)


def test_protect() -> None:
    """Test to take out directory from protected archive."""

    def individual_test(temporary_root: Path) -> None:
        _protect_test(
            temporary_root,
            _initialize_archive(temporary_root),
            _get_edit_protect(_get_archive_path(temporary_root)),
        )

    _inside_temporary_directory(individual_test)


def test_remove() -> None:
    """Test of directory used for removing process when archive is edited."""

    def individual_test(temporary_root: Path) -> None:
        _remove_test(
            temporary_root,
            _initialize_archive(temporary_root),
            _get_edit_remove(
                _get_archive_path(temporary_root),
                create_directory(_get_root_edit(temporary_root)),
            ),
        )

    _inside_temporary_directory(individual_test)
