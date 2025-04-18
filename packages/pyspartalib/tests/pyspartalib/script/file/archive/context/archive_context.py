#!/usr/bin/env python

"""User defined types using class "TypedDict"."""

from pathlib import Path
from typing import TypedDict

from pyspartalib.context.extension.path_context import Paths


class ArchiveStatus(TypedDict):
    """Class to represent an archive information.

    It's used for test to take out directory from inside of archive.
    """

    archive: Path
    take: Paths
    keep: Paths
