#!/usr/bin/env python

"""Test module to record paths which is source and destination pair."""

from collections.abc import Sized
from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.string_context import Strs
from pyspartalib.context.extension.path_context import (
    PathFunc,
    PathPair,
    PathPair2,
    Paths2,
    Paths3,
)
from pyspartalib.script.frame.current_frame import CurrentFrame
from pyspartalib.script.path.modify.current.get_relative import is_relative
from pyspartalib.script.path.safe.safe_file_history import FileHistory
from pyspartalib.script.time.directory.get_time_path import (
    get_initial_time_path,
)


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


def _length_error(result: Sized, expected: int) -> None:
    if len(result) != expected:
        raise ValueError


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _no_exists_error(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError


def _get_history_root(temporary_root: Path) -> Path:
    return Path(temporary_root, "history")


def _get_group() -> Strs:
    return [group + ".path" for group in ["source", "destination"]]


def _get_current_file() -> Path:
    return CurrentFrame().get_frame()["file"]


def _compare_path_pair(result: Path, expected: Path) -> None:
    _no_exists_error(result)
    _difference_error(result, expected)


def _compare_path_count(expected: PathPair2, result: PathPair2) -> None:
    _length_error({len(history) for history in [expected, result]}, 1)


def _take_out_path(history: PathPair2) -> Paths2:
    return [
        [value[group] for group in _get_group()] for value in history.values()
    ]


def _take_out_path_pair(expected: PathPair2, result: PathPair2) -> Paths3:
    return [_take_out_path(history) for history in [expected, result]]


def _compare_path_name(expected: PathPair2, result: PathPair2) -> None:
    _difference_error(*_take_out_path_pair(expected, result))


def _common_test(expected: PathPair2, result: PathPair2) -> None:
    _compare_path_count(expected, result)
    _compare_path_name(expected, result)


def _compare_added(expected: PathPair2, result: PathPair2 | None) -> None:
    _common_test(expected, _none_error(result))


def _compare_root(
    temporary_root: Path,
    date_time_root: Path,
    file_history: FileHistory,
) -> None:
    _compare_path_pair(
        file_history.get_history_root(),
        Path(temporary_root, date_time_root),
    )


def _relative_test(path: Path, root: Path) -> None:
    _no_exists_error(path)
    _fail_error(is_relative(path, root_path=root))


def _compare_path_before(file_history: FileHistory) -> None:
    _not_none_error(file_history.get_history_path())


def _compare_path_after(
    temporary_root: Path,
    file_history: FileHistory,
) -> None:
    _relative_test(
        _none_error(file_history.get_history_path()),
        temporary_root,
    )


def _compare_path(temporary_root: Path, file_history: FileHistory) -> None:
    _compare_path_before(file_history)
    file_history.get_history()
    _compare_path_after(temporary_root, file_history)


def _compare_history(file_history: FileHistory) -> None:
    _not_none_error(file_history.get_history())


def _get_expected(source_path: Path, destination_path: Path) -> PathPair:
    return dict(
        zip(_get_group(), [source_path, destination_path], strict=True),
    )


def _add_history(
    file_history: FileHistory,
    expected: PathPair2,
    name: str,
) -> None:
    source_path: Path = _get_current_file().parent.with_name("source.json")
    destination_path: Path = source_path.with_stem(name)

    file_history.add_history(source_path, destination_path)
    expected[name] = _get_expected(source_path, destination_path)


def _add_history_single(file_history: FileHistory) -> PathPair2:
    expected: PathPair2 = {}

    _add_history(file_history, expected, "single")

    return expected


def _add_history_array(file_history: FileHistory) -> PathPair2:
    expected: PathPair2 = {}

    for i in range(10):
        _add_history(file_history, expected, str(i).zfill(4))

    return expected


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def _get_file_history(working_root: Path, history_root: Path) -> FileHistory:
    return FileHistory(
        working_root=working_root,
        history_root=history_root,
        override=True,
    )


def test_work() -> None:
    """Test to compare user defined temporary working space."""

    def individual_test(temporary_root: Path) -> None:
        _compare_root(
            temporary_root,
            get_initial_time_path(),
            FileHistory(working_root=temporary_root, override=True),
        )

    _inside_temporary_directory(individual_test)


def test_history() -> None:
    """Test to compare user defined temporary working space.

    The path of working space include date time string.
    """

    def individual_test(temporary_root: Path) -> None:
        history_root: Path = _get_history_root(temporary_root)

        _compare_root(
            history_root,
            get_initial_time_path(),
            _get_file_history(temporary_root, history_root),
        )

    _inside_temporary_directory(individual_test)


def test_get() -> None:
    """Test to get current file operation history."""
    file_history = FileHistory()

    _compare_added(
        _add_history_single(file_history),
        file_history.get_history(),
    )

    _compare_history(file_history)


def test_single() -> None:
    """Test to record single source and destination path pair."""
    file_history = FileHistory()

    _compare_added(
        _add_history_single(file_history),
        file_history.close_history(),
    )


def test_array() -> None:
    """Test to record multiple source and destination path pair."""
    file_history = FileHistory()

    _compare_added(
        _add_history_array(file_history),
        file_history.close_history(),
    )


def test_path() -> None:
    """Test for specific directory for exporting paths you recorded."""

    def individual_test(temporary_root: Path) -> None:
        file_history = FileHistory(working_root=temporary_root)

        _add_history_array(file_history)
        _compare_path(temporary_root, file_history)

    _inside_temporary_directory(individual_test)
