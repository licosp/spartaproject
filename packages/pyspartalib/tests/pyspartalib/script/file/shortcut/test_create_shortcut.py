#!/usr/bin/env python

"""Test module to create Windows shortcut from PowerShell."""

from collections.abc import Sized
from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.default.string_context import Strs
from pyspartalib.context.extension.path_context import (
    PathFunc,
    PathPair,
    Paths,
)
from pyspartalib.context.type_context import Type
from pyspartalib.script.directory.date_time_space import create_working_space
from pyspartalib.script.file.shortcut.create_shortcut import create_shortcut
from pyspartalib.script.file.shortcut.get_shortcut import get_shortcut
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.path.modify.get_resource import get_resource
from pyspartalib.script.path.temporary.create_temporary_file import (
    create_temporary_file,
)
from pyspartalib.script.project.project_context import ProjectContext
from tests.pyspartalib.interface.pytest import raises


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _length_error(result: Sized, expected: int) -> None:
    if len(result) != expected:
        raise ValueError


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _no_exists_error(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError


def _get_config_file() -> Path:
    return get_resource(local_path=Path("forward.json"))


def _get_project_context() -> ProjectContext:
    return ProjectContext(forward=_get_config_file())


def _get_shared_paths() -> PathPair:
    return _get_project_context().get_path_context("shortcut")


def _get_temporary_windows() -> Path:
    return _get_shared_paths()["temporary.path"]


def _create_working_space() -> Path:
    return create_working_space(_get_temporary_windows(), jst=True)


def _create_shortcut(shortcut_target: Path, shortcut_path: Path) -> bool:
    return create_shortcut(
        shortcut_target,
        shortcut_path,
        forward=_get_config_file(),
    )


def _create_shortcut_remove(
    shortcut_target: Path,
    shortcut_path: Path,
    remove_root: Path,
) -> bool:
    return create_shortcut(
        shortcut_target,
        shortcut_path,
        remove_root=remove_root,
        forward=_get_config_file(),
    )


def _success_created(shortcut_target: Path, shortcut_path: Path) -> None:
    _fail_error(_create_shortcut(shortcut_target, shortcut_path))


def _success_created_remove(
    shortcut_target: Path,
    shortcut_path: Path,
    remove_root: Path,
) -> None:
    _fail_error(
        _create_shortcut_remove(shortcut_target, shortcut_path, remove_root),
    )


def _confirm_exists(shortcut_target: Path, shortcut_path: Path) -> None:
    for path in [shortcut_target, shortcut_path]:
        _no_exists_error(path)


def _compare_name(shortcut_target: Path, shortcut_path: Path) -> None:
    _difference_error(shortcut_target.name, shortcut_path.stem)


def _common_test(shortcut_target: Path, shortcut_path: Path) -> None:
    _confirm_exists(shortcut_target, shortcut_path)
    _compare_name(shortcut_target, shortcut_path)


def _get_shortcut_names(roots: Paths) -> Strs:
    return [
        path.name
        for root in roots
        for path in walk_iterator(root, directory=False, suffix="lnk", depth=1)
    ]


def _compare_shortcut_names(shortcut_root: Path, remove_root: Path) -> None:
    _length_error(set(_get_shortcut_names([shortcut_root, remove_root])), 1)


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_file() -> None:
    """Test to create file type shortcut of Windows from PowerShell."""
    working_space: Path = _create_working_space()
    shortcut_target: Path = create_temporary_file(working_space)
    shortcut_path: Path = get_shortcut(shortcut_target, working_space)

    _success_created(shortcut_target, shortcut_path)
    _common_test(shortcut_target, shortcut_path)


def test_directory() -> None:
    """Test to create directory type shortcut of Windows from PowerShell."""
    shortcut_target: Path = _create_working_space()
    shortcut_path: Path = get_shortcut(shortcut_target, shortcut_target)

    _success_created(shortcut_target, shortcut_path)
    _common_test(shortcut_target, shortcut_path)


def test_exist() -> None:
    """Test to exists shortcut file before create it."""
    empty_path: Path = Path("empty")

    with raises(FileNotFoundError):
        create_shortcut(empty_path, empty_path)


def test_remove() -> None:
    """Test to remove shortcut file when overriding existing shortcut."""
    working_space: Path = _create_working_space()
    shortcut_target: Path = create_temporary_file(working_space)
    shortcut_path: Path = get_shortcut(shortcut_target, working_space)

    _success_created(shortcut_target, shortcut_path)

    def individual_test(temporary_root: Path) -> None:
        _success_created_remove(shortcut_target, shortcut_path, temporary_root)
        _compare_shortcut_names(working_space, temporary_root)

    _inside_temporary_directory(individual_test)
