#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to create temporary working directory shared in class."""

from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp


class WorkSpace:
    """Class to create temporary working directory shared in class."""

    def _initialize_variables(self, working_root: Path | None) -> None:
        if working_root is None:
            working_root = Path(mkdtemp())

        self._work_space_root: Path = working_root

    def get_root(self) -> Path:
        """Get root path of temporary working directory."""
        return self._work_space_root

    def __del__(self) -> None:
        """Remove temporary working directory."""
        rmtree(str(self._work_space_root))

    def __init__(self, working_root: Path | None = None) -> None:
        """Create temporary working directory."""
        self._initialize_variables(working_root)
