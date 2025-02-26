#!/usr/bin/env python

"""Test module to compare two dictionaries which store path and time stamp."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.extension.path_context import PathFunc
from pyspartalib.context.extension.time_context import TimePair, TimePair2
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.path.modify.current.get_relative import get_relative
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from pyspartalib.script.time.path.get_timestamp import get_directory_latest
from pyspartalib.script.time.stamp.is_same_stamp import is_same_stamp


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_directory_latest(path: Path, access: bool) -> TimePair:
    return get_directory_latest(walk_iterator(path), access=access)


def _get_relative_text(path_text: str, root_path: Path) -> str:
    return str(get_relative(Path(path_text), root_path=root_path))


def _get_relative_latest(path: Path, access: bool = False) -> TimePair:
    return {
        _get_relative_text(path_text, path): time
        for path_text, time in _get_directory_latest(path, access).items()
    }


def _is_access(group: str) -> bool:
    return group == "access"


def _get_stamp_pair(stamp_root: Path) -> TimePair2:
    return {
        group: _get_relative_latest(stamp_root, access=_is_access(group))
        for group in ["update", "access"]
    }


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_same() -> None:
    """Test to compare two dictionaries about latest date time you got."""

    def individual_test(temporary_root: Path) -> None:
        stamp_pair: TimePair2 = _get_stamp_pair(
            create_temporary_tree(Path(temporary_root, "tree")),
        )

        _fail_error(
            is_same_stamp(stamp_pair["update"], stamp_pair["access"]),
        )

    _inside_temporary_directory(individual_test)
