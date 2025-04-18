#!/usr/bin/env python

"""Test module to create symbolic link and link information."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.extension.path_context import PathFunc, Paths, Paths2
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.path.modify.current.get_relative import get_relative
from pyspartalib.script.path.symbolic.context.symbolic_context import (
    SymbolicLink,
)
from pyspartalib.script.path.symbolic.create_symbolic import (
    create_symbolic_link,
    get_symbolic_link,
)
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_expected_paths() -> Paths:
    return [Path(group) for group in ["source", "symbolic"]]


def _create_symbolic(path: Path) -> SymbolicLink:
    return create_symbolic_link(
        create_temporary_tree(Path(path, "source"), tree_deep=1),
        Path(path, "symbolic"),
    )


def _get_symbolic_paths(symbolic_link: SymbolicLink) -> Paths:
    return [symbolic_link["source"], symbolic_link["symbolic"]]


def _get_relative_paths(working_root: Path) -> Paths:
    return [
        get_relative(path, root_path=working_root)
        for path in walk_iterator(working_root)
    ]


def _get_relative_pair(symbolic_link: SymbolicLink) -> Paths2:
    return [
        _get_relative_paths(working_root)
        for working_root in _get_symbolic_paths(symbolic_link)
    ]


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_path() -> None:
    """Test to get type that represent paths about symbolic link."""
    expected_paths: Paths = _get_expected_paths()

    _difference_error(
        _get_symbolic_paths(get_symbolic_link(*expected_paths)),
        expected_paths,
    )


def test_create() -> None:
    """Test to create symbolic link and link information."""

    def individual_test(temporary_root: Path) -> None:
        symbolic_link: SymbolicLink = _create_symbolic(temporary_root)

        _fail_error(symbolic_link["symbolic"].is_symlink())
        _difference_error(*_get_relative_pair(symbolic_link))

    _inside_temporary_directory(individual_test)
