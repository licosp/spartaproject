#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test module to get path of a shortcut file on Windows environment."""

from pathlib import Path

from pyspartaproj.script.file.shortcut.get_shortcut import get_shortcut


def _get_target_root() -> Path:
    return Path("root", "create")


def test_directory() -> None:
    """Test to get path of a shortcut file that target is directory."""
    target_path: Path = Path(_get_target_root(), "target")
    shortcut_root: Path = Path("root", "created")
    expected: Path = Path("root", "created", "target.lnk")

    assert expected == get_shortcut(target_path, shortcut_root)
