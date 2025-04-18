#!/usr/bin/env python

"""Test module to import a context of whole project from outside Json."""

from collections.abc import Sized
from pathlib import Path

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.integer_context import IntPair
from pyspartalib.context.default.string_context import StrPair, Strs, Strs2
from pyspartalib.context.extension.path_context import PathPair
from pyspartalib.script.path.modify.get_resource import get_resource
from pyspartalib.script.platform.platform_status import get_platform
from pyspartalib.script.project.project_context import ProjectContext


def _length_error(result: Sized, expected: int) -> None:
    if len(result) != expected:
        raise ValueError


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_expected_numbers() -> IntPair:
    return {"index": 0, "count": 1}


def _get_expected_strings() -> StrPair:
    return {"name": "name", "language": "language"}


def _get_expected_paths() -> PathPair:
    return {
        "root.path": Path("root"),
        "head.path": Path("root", "head"),
    }


def _common_test(keys_pair: Strs2) -> None:
    _length_error({str(sorted(keys)) for keys in keys_pair}, 1)


def _get_config_file() -> Path:
    return get_resource(local_path=Path("project_context", "forward.json"))


def _import_context() -> ProjectContext:
    return ProjectContext(forward=_get_config_file())


def _platform_key_test(platform: str, project: ProjectContext) -> None:
    expected: Strs = ["group", "type"]
    context_key: str = project.get_platform_key(expected)
    key_elements: Strs = context_key.split("_")

    _difference_error(key_elements[:2], expected)
    _difference_error(key_elements[-1], platform)


def _add_platform(file: str) -> str:
    return file + "_" + get_platform()


def _get_expected_path(path_roots: Strs, path_heads: Strs) -> Path:
    return Path(
        *[
            Path(*[root, _add_platform(head)])
            for root, head in zip(path_roots, path_heads, strict=True)
        ],
    )


def test_bool() -> None:
    """Test to filter and get project context by boolean type."""
    _fail_error(ProjectContext().get_bool_context("test")["boolean"])


def test_integer() -> None:
    """Test to filter and get project context by integer type."""
    expected: IntPair = _get_expected_numbers()

    project: ProjectContext = _import_context()
    integer_context: IntPair = project.get_integer_context("type")

    _common_test([list(items.keys()) for items in [expected, integer_context]])

    for key, value in expected.items():
        _difference_error(integer_context[key], value)


def test_string() -> None:
    """Test to filter and get project context by string type."""
    expected: StrPair = _get_expected_strings()

    project: ProjectContext = _import_context()
    string_context: StrPair = project.get_string_context("type")

    _common_test([list(items.keys()) for items in [expected, string_context]])

    for key, value in expected.items():
        _difference_error(string_context[key], value)


def test_path() -> None:
    """Test to filter and get project context by path type."""
    expected: PathPair = _get_expected_paths()

    project: ProjectContext = _import_context()
    path_context: PathPair = project.get_path_context("type")

    _common_test([list(items.keys()) for items in [expected, path_context]])

    for key, value in expected.items():
        _difference_error(path_context[key], value)


def test_key() -> None:
    """Test to get key of project context file corresponding to platform."""
    _platform_key_test(
        get_platform(),
        ProjectContext(forward=_get_config_file()),
    )


def test_platform() -> None:
    """Test to get key of project context file.

    The key is corresponding to specific platform.
    """
    for platform in ["linux", "windows"]:
        _platform_key_test(
            platform,
            ProjectContext(forward=_get_config_file(), platform=platform),
        )


def test_directory() -> None:
    """Test to get path which is merged by multiple directories."""
    path_roots: Strs = ["root", "directory"]
    path_heads: Strs = ["body", "head"]

    _difference_error(
        _import_context().merge_paths("project", path_roots),
        _get_expected_path(path_roots, path_heads),
    )
