#!/usr/bin/env python

"""Module to get latest date time of file or directory as time object."""

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from pyspartalib.context.extension.path_context import PathGene
from pyspartalib.context.extension.time_context import TimePair
from pyspartalib.script.time.epoch.from_timestamp import time_from_timestamp
from pyspartalib.script.time.path.get_file_epoch import get_file_epoch


def _convert_timestamp(time: float, jst: bool) -> datetime:
    return time_from_timestamp(Decimal(str(time)), jst=jst)


def _get_latest_times(
    walk_generator: PathGene,
    access: bool = False,
    jst: bool = False,
) -> TimePair:
    return {
        str(path): get_latest(path, jst=jst, access=access)
        for path in walk_generator
    }


def get_invalid_time() -> datetime:
    """Get invalid time date which is used for comparing time you got.

    Returns:
        datetime: Invalid time date.

    """
    return datetime(1, 1, 1, tzinfo=UTC)


def get_latest(
    path: Path,
    access: bool = False,
    jst: bool = False,
) -> datetime:
    """Get latest date time of file or directory as time object.

    Args:
        path (Path): Path of file or directory you want to get date time.
            It's used for argument "path" of function "get_file_epoch".

        access (bool, optional): Defaults to False.
            Return update time if it's False, and access time if True.
            It's used for argument "access" of function "get_file_epoch".

        jst (bool, optional): Defaults to False.
            Return latest date time as JST time zone if it's True.

    Returns:
        datetime: Latest date time as time object.
            Return unique invalid time if time you got is broke is exists.

    """
    if time := get_file_epoch(path, access=access):
        return _convert_timestamp(float(time), jst=jst)

    return get_invalid_time()


def get_directory_latest(
    walk_generator: PathGene,
    access: bool = False,
    jst: bool = False,
) -> TimePair:
    """Get array of latest date time in selected directory as time object.

    Args:
        walk_generator (PathGene):
            Path generator you want to get latest date time inside.

        access (bool, optional): Defaults to False.
            Return update time if it's False, and access time if True.

        jst (bool, optional): Defaults to False.
            Return latest date time as JST time zone if it's True.

    Returns:
        TimePair: Dictionary constructed by string path and latest date time.
            Return unique invalid time if time you got is broke is exists.

    """
    return _get_latest_times(walk_generator, access, jst)
