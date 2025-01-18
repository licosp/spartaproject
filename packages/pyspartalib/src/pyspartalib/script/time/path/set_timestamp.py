#!/usr/bin/env python

"""Module to set latest date time of file or directory by time object."""

from datetime import datetime
from decimal import Decimal
from os import utime
from pathlib import Path

from pyspartalib.context.default.float_context import Floats
from pyspartalib.context.extension.decimal_context import Decs
from pyspartalib.script.decimal.convert_float import convert_float_array
from pyspartalib.script.time.path.get_file_epoch import get_file_epoch
from pyspartalib.script.time.stamp.offset_timezone import offset_time


def _convert_timestamp(time: datetime) -> Decimal:
    return Decimal(str(offset_time(time).timestamp()))


def _get_file_date_time(path: Path, time: datetime, access: bool) -> Floats:
    return convert_float_array(_get_path_times(path, time, access))


def _get_path_times(path: Path, time: datetime, access: bool) -> Decs:
    path_times: Decs = [_convert_timestamp(time)]

    if time_epoch := get_file_epoch(path, access=(not access)):
        path_times += [time_epoch]

    if not access:
        path_times.reverse()

    return path_times


def _set_time(path: Path, access: float, update: float) -> Path:
    utime(path, (access, update))
    return path


def set_invalid(path: Path) -> Path:
    return _set_time(path, 0.0, 0.0)


def set_latest(path: Path, time: datetime, access: bool = False) -> Path:
    """Set latest date time of file or directory by time object.

    Args:
        path (Path): Path of file or directory you want to set date time.

        time (datetime): Latest date time you want to set.

        access (bool, optional): Defaults to False.
            Set update time if it's False, and access time if True.

    Returns:
        Path: Path of file or directory you set latest date time.

    """
    return _set_time(path, *_get_file_date_time(path, time, access))
