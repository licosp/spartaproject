#!/usr/bin/env python

"""Test module to create temporary working space including date time string."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.script.directory.date_time_space import create_working_space
from pyspartalib.script.path.modify.current.get_relative import get_relative
from pyspartalib.script.time.directory.get_time_path import (
    get_initial_time_path,
)


def _path_name_error(expected: Path, result: Path) -> None:
    if expected != result:
        raise ValueError


def _compare_time_path(result: Path) -> None:
    _path_name_error(get_initial_time_path(), result)


def test_create() -> None:
    """Test to create temporary working space including date time string."""
    with TemporaryDirectory() as temporary_directory:
        temporary_path: Path = Path(temporary_directory)
        time_path: Path = create_working_space(temporary_path, override=True)

        assert time_path.exists()

        _compare_time_path(get_relative(time_path, root_path=temporary_path))
