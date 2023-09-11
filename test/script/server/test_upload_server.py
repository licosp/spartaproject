#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Callable

from script.directory.create_directory import create_directory
from script.path.temporary.create_temporary_file import create_temporary_file
from script.path.temporary.create_temporary_tree import create_temporary_tree
from script.server.upload_server import UploadServer


def _common_test(server: UploadServer, source_path: Path) -> None:
    assert server.upload(source_path)


def _inside_temporary_directory(
    function: Callable[[UploadServer], None]
) -> None:
    server: UploadServer = UploadServer()

    if server.connect():
        function(server)


def test_file() -> None:
    def individual_test(server: UploadServer) -> None:
        temporary_path: Path = server.get_working_space()
        _common_test(server, create_temporary_file(temporary_path))

    _inside_temporary_directory(individual_test)


def test_directory() -> None:
    def individual_test(server: UploadServer) -> None:
        temporary_path: Path = server.get_working_space()
        source_path: Path = create_directory(Path(temporary_path, 'directory'))
        _common_test(server, source_path)

    _inside_temporary_directory(individual_test)


def test_tree() -> None:
    def individual_test(server: UploadServer) -> None:
        temporary_path: Path = server.get_working_space()
        source_path: Path = Path(temporary_path, 'tree')
        create_temporary_tree(source_path, tree_deep=2)
        _common_test(server, source_path)

    _inside_temporary_directory(individual_test)


def main() -> bool:
    test_file()
    test_directory()
    test_tree()
    return True
