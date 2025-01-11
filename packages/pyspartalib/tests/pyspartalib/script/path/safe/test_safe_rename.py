#!/usr/bin/env python

"""Test module to rename file or directory and log history."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.custom.rename_context import RenamePathFunc
from pyspartalib.context.default.bool_context import BoolPair
from pyspartalib.context.extension.path_context import PathPair2
from pyspartalib.script.bool.same_value import bool_same_array
from pyspartalib.script.directory.create_directory import create_directory
from pyspartalib.script.path.safe.safe_rename import SafeRename
from pyspartalib.script.path.status.check_exists import check_exists_pair
from pyspartalib.script.path.temporary.create_temporary_file import (
    create_temporary_file,
)
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from tests.pyspartalib.interface.pytest import fail


def _compare_empty(history: PathPair2 | None) -> PathPair2:
    if history is None:
        fail()

    assert len(history) == 1

    return history


def _common_test(history: PathPair2 | None) -> None:
    for path_pair in _compare_empty(history).values():
        exists_pair: BoolPair = check_exists_pair(path_pair)
        assert bool_same_array(
            [not exists_pair["source.path"], exists_pair["destination.path"]],
        )


def _inside_temporary_directory(function: RenamePathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(SafeRename(), Path(temporary_path))


def _rename(safe_rename: SafeRename, path: Path) -> PathPair2 | None:
    safe_rename.rename(path, path.with_stem("destination"))
    return safe_rename.close_history()


def test_file() -> None:
    """Test to rename file, and log history."""

    def individual_test(safe_rename: SafeRename, temporary_path: Path) -> None:
        _common_test(
            _rename(safe_rename, create_temporary_file(temporary_path)),
        )

    _inside_temporary_directory(individual_test)


def test_override() -> None:
    """Test to rename file for the situation that destination is existing."""

    def individual_test(safe_rename: SafeRename, temporary_path: Path) -> None:
        source_path: Path = create_temporary_file(temporary_path)
        destination_path: Path = safe_rename.rename(
            source_path,
            source_path,
            override=True,
        )
        expected: Path = source_path.with_stem(source_path.stem + "_")

        _common_test(safe_rename.close_history())
        assert expected == destination_path

    _inside_temporary_directory(individual_test)


def test_directory() -> None:
    """Test to rename directory, and log history."""

    def individual_test(safe_rename: SafeRename, temporary_path: Path) -> None:
        _common_test(
            _rename(
                safe_rename,
                create_directory(Path(temporary_path, "temporary")),
            ),
        )

    _inside_temporary_directory(individual_test)


def test_tree() -> None:
    """Test to rename files and directories, and log history."""

    def individual_test(safe_rename: SafeRename, temporary_path: Path) -> None:
        _common_test(
            _rename(
                safe_rename,
                create_temporary_tree(
                    Path(temporary_path, "temporary"),
                    tree_deep=2,
                ),
            ),
        )

    _inside_temporary_directory(individual_test)
