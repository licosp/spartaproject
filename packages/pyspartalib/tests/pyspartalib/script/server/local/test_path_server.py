#!/usr/bin/env python

"""Test module to handle paths about file and directory on server."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.extension.path_context import PathFunc
from pyspartalib.context.type_context import Type
from pyspartalib.script.server.local.path_server import PathServer
from pyspartalib.script.time.directory.get_time_path import (
    get_initial_time_path,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _exists_error(path: Path) -> None:
    if not path.exists():
        raise ValueError


def _get_local_root(temporary_root: Path) -> Path:
    return Path(temporary_root, "local")


def _compare_relative(
    expected: Path,
    result: Path,
    server: PathServer,
) -> None:
    _difference_error(server.to_relative_path(result), expected)


def _compare_path(result: Path, expected: Path) -> None:
    _exists_error(result)
    _difference_error(result, expected)


def _compare_working(
    temporary_root: Path,
    date_time: Path,
    server: PathServer,
) -> None:
    _compare_path(
        server.get_date_time_root(),
        Path(
            temporary_root,
            server.get_path("work_root"),
            date_time,
        ),
    )


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_table() -> None:
    """Test to get keys of predefined all paths about server."""
    expected: int = 6
    server = PathServer()

    assert expected == len(list(server.get_path_table()))


def test_path() -> None:
    """Test to get all paths about server."""
    server = PathServer()

    for path in server.get_path_table():
        server.get_path(path)


def test_work() -> None:
    """Test for user defined temporary working space to connect server."""

    def individual_test(temporary_root: Path) -> None:
        server = PathServer(working_root=temporary_root)
        _compare_path(server.get_local_root(), temporary_root)

    _inside_temporary_directory(individual_test)


def test_local() -> None:
    """Test for user defined local directory to connect server."""

    def individual_test(temporary_root: Path) -> None:
        local_root: Path = _get_local_root(temporary_root)
        server = PathServer(working_root=temporary_root, local_root=local_root)
        _compare_path(server.get_local_root(), local_root)

    _inside_temporary_directory(individual_test)


def test_date() -> None:
    """Test for temporary working space including date time string."""
    date_time: Path = get_initial_time_path()

    def individual_test(temporary_root: Path) -> None:
        local_root: Path = _get_local_root(temporary_root)
        server = PathServer(
            working_root=temporary_root,
            local_root=local_root,
            override=True,
        )
        _compare_working(local_root, date_time, server)

    _inside_temporary_directory(individual_test)


def test_relative() -> None:
    """Test to convert full path to relative path.

    The full path of directory is based on local temporary working space.
    """
    expected: Path = Path("temp")
    server = PathServer()

    _compare_relative(
        expected,
        Path(server.get_local_root(), expected),
        server,
    )


def test_full() -> None:
    """Test to convert relative path to full path.

    The full path of directory is based on local temporary working space.
    """
    expected: Path = Path("temp")
    server = PathServer()

    _compare_relative(expected, server.to_full_path(expected), server)
