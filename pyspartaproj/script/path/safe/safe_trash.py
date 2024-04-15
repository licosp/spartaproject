#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to remove file or directory and log history."""

from pathlib import Path

from pyspartaproj.context.extension.path_context import Paths
from pyspartaproj.script.directory.create_directory_parent import (
    create_directory_parent,
)
from pyspartaproj.script.path.modify.get_relative import get_relative
from pyspartaproj.script.path.safe.safe_rename import SafeRename


class SafeTrash(SafeRename):
    """Class to remove file or directory and log history."""

    def _move_file(self, target: Path, root: Path) -> None:
        if target.exists():
            trash_path: Path = Path(
                self.history_path, get_relative(target, root_path=root)
            )
            create_directory_parent(trash_path)
            self.rename(target, trash_path, override=True)

    def trash(self, trash_path: Path, trash_root: Path | None = None) -> Path:
        """Remove file or directory and log history.

        Args:
            trash_path (Path): Path you want to remove.

            trash_root (Path | None, optional): Defaults to None.
                Path of trash box directory.

        Returns:
            Path: "trash_path" is returned.
        """
        parent_root: Path = trash_path.parent

        if trash_root is None:
            self._move_file(trash_path, parent_root)
        elif trash_path.is_relative_to(trash_root):
            self._move_file(trash_path, trash_root)
        else:
            self._move_file(trash_path, parent_root)

        return trash_path

    def trash_at_once(
        self, trash_paths: Paths, trash_root: Path | None = None
    ) -> Paths:
        """Remove files or directories at once, and log history.

        Args:
            trash_paths (Paths): Paths you want to remove.

            trash_root (Path | None, optional): Defaults to None.
                Path of trash box directory.
                It's used for argument "trash_root" of method "trash".

        Returns:
            Paths: "trash_paths" is returned.
        """
        for trash_path in trash_paths:
            self.trash(trash_path, trash_root=trash_root)

        return trash_paths

    def __init__(self, remove_root: Path | None = None) -> None:
        """Initialize variables and super class.

        Args:
            remove_root (Path | None, optional): Defaults to None.
                Directory you want to places removed file or directory.
        """
        super().__init__(history_path=remove_root)
