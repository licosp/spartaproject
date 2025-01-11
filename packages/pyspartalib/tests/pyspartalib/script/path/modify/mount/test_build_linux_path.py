#!/usr/bin/env python

"""Test module to get path about Windows mounted on Linux."""

from pathlib import Path

from pyspartalib.context.type_context import Type
from pyspartalib.script.path.modify.mount.build_linux_path import (
    get_linux_head,
    get_linux_path,
    get_mount_point,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_drive_letter() -> str:
    return "c"


def _get_relative_root() -> Path:
    return Path("root", "body", "head")


def _get_linux_head() -> Path:
    return get_linux_head(_get_drive_letter())


def _get_linux_path() -> Path:
    return get_linux_path(_get_drive_letter(), _get_relative_root())


def _get_expected_mount() -> Path:
    return Path("/", "mnt")


def _get_expected_head() -> Path:
    return Path(get_mount_point(), _get_drive_letter())


def _get_expected_path() -> Path:
    return Path(_get_expected_head(), _get_relative_root())


def _compare_path(expected: Path, result: Path) -> None:
    assert expected == result


def test_mount() -> None:
    """Test to get the path of a mount point of Linux."""
    _difference_error(get_mount_point(), _get_expected_mount())


def test_head() -> None:
    """Test to get path of a drive letter about Windows mounted on Linux."""
    _difference_error(_get_linux_head(), _get_expected_head())


def test_path() -> None:
    """Test to generate path about Windows mounted on Linux from elements."""
    _difference_error(_get_linux_path(), _get_expected_path())
