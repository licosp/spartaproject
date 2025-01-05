#!/usr/bin/env python

"""Module to read Windows shortcut information from PowerShell."""

from pathlib import Path

from pyspartalib.context.default.string_context import StrGene, Strs
from pyspartalib.script.path.modify.get_resource import get_resource
from pyspartalib.script.path.modify.mount.convert_to_linux import (
    convert_to_linux,
)
from pyspartalib.script.path.modify.mount.convert_to_windows import (
    convert_to_windows,
)
from pyspartalib.script.platform.platform_status import is_platform_linux
from pyspartalib.script.shell.execute_powershell import (
    execute_powershell,
    get_double_quoted_command,
    get_path_string,
    get_quoted_path,
    get_script_string,
)


def _convert_to_linux(path: Path) -> Path:
    if is_platform_linux():
        return convert_to_linux(path)

    return path


def _convert_to_windows(path: Path) -> Path:
    if is_platform_linux():
        return convert_to_windows(path)

    return path


def _convert_to_path(path_text: str) -> Path:
    return Path(path_text.replace("\\", "/"))


def _get_script_string() -> str:
    return get_script_string(get_resource(local_path=Path("read.ps1")))


def _get_quoted_path(path: Path) -> str:
    return get_quoted_path(get_path_string(_convert_to_windows(path)))


def _get_shortcut_command(shortcut_path: Path) -> str:
    return get_double_quoted_command(
        [_get_script_string(), _get_quoted_path(shortcut_path)],
    )


def _execute_script(
    shortcut_path: Path,
    platform: str | None,
    forward: Path | None,
) -> StrGene:
    return execute_powershell(
        [_get_shortcut_command(shortcut_path)],
        platform=platform,
        forward=forward,
    )


def _no_exists_error(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError


def _cleanup_result(result: Strs) -> Path | None:
    if len(result) == 1:
        return _convert_to_linux(_convert_to_path(result[0]))

    return None


def read_shortcut(
    shortcut_path: Path,
    platform: str | None = None,
    forward: Path | None = None,
) -> Path | None:
    """Read Windows shortcut information from PowerShell.

    Args:
        shortcut_path (Path): Path of shortcut you want to read inside.

        platform (str | None, optional): Defaults to None.
            You can select an execution platform from "linux" or "windows".
            Current execution platform is selected if argument is None.
            It's used for argument "platform" of function "execute_powershell".

        forward (Path | None, optional): Defaults to None.
            Path of setting file in order to place
                project context file to any place.
            It's used for argument "forward" of function "execute_powershell".

    Returns:
        Path | None: Path which is a link destination of shortcut.

    """
    _no_exists_error(shortcut_path)

    return _cleanup_result(
        list(_execute_script(shortcut_path, platform, forward)),
    )
