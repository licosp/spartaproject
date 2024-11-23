#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from pyspartaproj.script.path.modify.mount.build_linux_path import (
    get_linux_head,
    get_linux_path,
    get_mount_point,
)


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
    _compare_path(_get_expected_mount(), get_mount_point())


def test_head() -> None:
    _compare_path(_get_expected_head(), _get_linux_head())
