#!/usr/bin/env python

"""Test module to check existing of files or directories."""

from pathlib import Path

from pyspartalib.context.default.bool_context import BoolPair, Bools
from pyspartalib.context.extension.path_context import PathPair, Paths
from pyspartalib.script.bool.compare_value import (
    bool_compare_array,
    bool_compare_pair,
)
from pyspartalib.script.frame.current_frame import CurrentFrame
from pyspartalib.script.path.status.check_exists import (
    check_exists_array,
    check_exists_pair,
)


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_current_file() -> Path:
    return CurrentFrame().get_frame()["file"]


def _get_unknown_file(path: Path) -> Path:
    return path.with_name("unknown.py")


def _get_expected_array() -> Bools:
    return [True, False]


def _get_expected_pair() -> BoolPair:
    return {"R": True, "G": False, "B": True}


def _get_source_array() -> Paths:
    current_file: Path = _get_current_file()
    return [current_file, _get_unknown_file(current_file)]


def _get_source_pair() -> PathPair:
    current_file: Path = _get_current_file()
    return {
        "R": current_file,
        "G": _get_unknown_file(current_file),
        "B": current_file.parent,
    }


def test_array() -> None:
    """Test to check existing of list of file or directory."""
    _fail_error(
        bool_compare_array(
            _get_expected_array(),
            check_exists_array(_get_source_array()),
        ),
    )


def test_pair() -> None:
    """Test to check existing of directory of file or directory."""
    _fail_error(
        bool_compare_pair(
            _get_expected_pair(),
            check_exists_pair(_get_source_pair()),
        ),
    )
