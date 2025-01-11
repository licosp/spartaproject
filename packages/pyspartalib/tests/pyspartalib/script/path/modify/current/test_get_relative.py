#!/usr/bin/env python

"""Test module to convert absolute path to relative."""

from pathlib import Path

from pyspartalib.context.default.bool_context import Bools
from pyspartalib.context.default.string_context import Strs
from pyspartalib.context.extension.path_context import PathPair, Paths
from pyspartalib.context.type_context import Type
from pyspartalib.script.bool.compare_value import bool_compare_array
from pyspartalib.script.bool.same_value import bool_same_array
from pyspartalib.script.path.modify.current.get_absolute import (
    get_absolute,
    get_absolute_array,
    get_absolute_pair,
)
from pyspartalib.script.path.modify.current.get_relative import (
    get_relative,
    get_relative_array,
    get_relative_pair,
    is_relative,
    is_relative_array,
)
from tests.pyspartalib.interface.pytest import raises


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_error() -> Path:
    return Path("error")


def _get_current_file() -> Path:
    return Path(__file__)


def _get_expected() -> Bools:
    return [True, False]


def _get_paths(current: Path) -> Paths:
    return [current, _get_error()]


def _to_pair(path_types: Strs, paths: Paths) -> PathPair:
    return {
        path_type: path
        for path_type, path in zip(path_types, paths, strict=True)
    }


def test_check() -> None:
    """Test to check path which is type relative."""
    current: Path = _get_current_file()

    assert bool_compare_array(
        _get_expected(),
        [
            is_relative(path, root_path=current.parent)
            for path in _get_paths(current)
        ],
    )


def test_check_array() -> None:
    """Test to check that list of paths are type relative at once."""
    current: Path = _get_current_file()

    assert bool_compare_array(
        _get_expected(),
        is_relative_array(_get_paths(current), root_path=current.parent),
    )


def test_unmatch() -> None:
    """Test to convert absolute path, but using invalid path."""
    with raises(ValueError):
        get_relative(_get_error())


def test_single() -> None:
    """Test to convert absolute path by using specific root path."""
    expected: Path = _get_current_file()
    _difference_error(get_absolute(get_relative(expected)), expected)


def test_root() -> None:
    """Test to convert absolute path with specific root."""
    expected_base: Path = _get_current_file()

    _difference_error(
        get_relative(expected_base, root_path=expected_base.parent),
        Path(expected_base.name),
    )


def test_array() -> None:
    """Test to convert list of absolute paths to relative."""
    expected_base: Path = _get_current_file()
    expected: Paths = [expected_base.parents[i] for i in range(3)]

    _difference_error(
        get_absolute_array(get_relative_array(expected)),
        expected,
    )


def test_pair() -> None:
    """Test to convert dictionary of absolute paths to relative."""
    expected_base: Path = _get_current_file()
    keys: Strs = ["R", "G", "B"]

    expected: PathPair = _to_pair(
        keys,
        [expected_base.parents[i] for i in range(3)],
    )
    result: PathPair = get_absolute_pair(get_relative_pair(expected))

    for key in keys:
        _difference_error(expected[key], result[key])
