#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to convert shared path between Linux and Windows."""

from pathlib import Path

from pyspartaproj.script.path.modify.current.get_relative import (
    get_relative,
    is_relative,
)


def _get_mount_root() -> Path:
    return Path("/", "mnt")


def _get_drive_identifier(path: Path) -> str:
    relative_path: Path = get_relative(path, root_path=_get_mount_root())
    return relative_path.parts[0].capitalize()


def _get_relative_root(path: Path) -> Path:
    relative_path: Path = get_relative(path, root_path=_get_mount_root())
    return Path(*relative_path.parts[1:])


def convert_mount(path: Path) -> Path:
    """Convert shared path between Linux and Windows.

    e.g., if you select argument (path) like "/mnt/c/Users/user",
        "C:/Users/user" is returned.

    Args:
        path (Path): Linux path which is starts from mount string.

    Returns:
        Path: Converted Windows path which is starts from drive letter.
    """
    mount_root: Path = _get_mount_root()

    if not is_relative(path, root_path=mount_root):
        return path

    drive_identifier: str = _get_drive_identifier(path)
    relative_root: Path = _get_relative_root(path)

    return Path(drive_identifier + ":", relative_root)
