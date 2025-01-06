#!/usr/bin/env python

"""Test module to execute CLI (Command Line Interface) script on subprocess."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.callable_context import Type
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.path.modify.current.get_current import get_current
from pyspartalib.script.shell.execute_command import (
    execute_multiple,
    execute_single,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _no_exists_error(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError


def _get_current() -> Strs:
    return list(execute_single(["pwd"]))


def _move_and_get(expected: Path) -> Strs:
    return list(
        execute_multiple([["cd", expected.as_posix()], ["pwd"]]),
    )


def test_single() -> None:
    """Test to execute generic script.

    Suppose that the test environment of Windows
        can execute simple Linux commands.
    """
    result: Strs = _get_current()

    _difference_error(len(result), 1)

    current: Path = Path(result[0])

    _no_exists_error(current)
    _difference_error(current, get_current())


def test_multiple() -> None:
    """Test to execute generic script which is multiple lines.

    Suppose that the test environment of Windows
        can execute simple Linux commands.
    """
    with TemporaryDirectory() as temporary_directory:
        expected: Path = Path(temporary_directory)
        result: Strs = _move_and_get(expected)

        _difference_error(len(result), 1)
        _difference_error(Path(result[0]), expected)
