#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test module to upload file or directory by SFTP functionality."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

from pyspartaproj.script.directory.create_directory import create_directory
from pyspartaproj.script.directory.date_time_space import get_working_space
from pyspartaproj.script.path.temporary.create_temporary_file import (
    create_temporary_file,
)
from pyspartaproj.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from pyspartaproj.script.server.local.upload_server import UploadServer


def _upload_path(server: UploadServer, source_path: Path) -> None:
    assert server.upload(source_path)


def _is_connect(server: UploadServer) -> None:
    assert server.connect()


def _get_server() -> UploadServer:
    return UploadServer(jst=True)


def _get_server_local(local_root: Path) -> UploadServer:
    return UploadServer(jst=True, local_root=local_root)


def _inside_temporary_directory(function: Callable[[Path], None]) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_file() -> None:
    """Test to upload single file to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(server, create_temporary_file(server.get_working_root()))


def test_directory() -> None:
    """Test to upload single directory to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(
        server, create_directory(Path(server.get_working_root(), "directory"))
    )


def test_tree() -> None:
    """Test to upload multiple files and directories to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(
        server,
        create_temporary_tree(
            Path(server.get_working_root(), "tree"), tree_deep=2
        ),
    )


def test_place() -> None:
    """Test to upload single file from selected local root to server."""

    def individual_test(temporary_root: Path) -> None:
        server: UploadServer = _get_server_local(temporary_root)
        _is_connect(server)

        working_path: Path = server.get_working_root()
        source_path: Path = create_temporary_file(
            Path(temporary_root, working_path)
        )

        assert server.upload(
            source_path, destination=Path(working_path, source_path.name)
        )

    _inside_temporary_directory(individual_test)


def main() -> bool:
    """Run all tests.

    Returns:
        bool: Success if get to the end of function.
    """
    test_file()
    test_directory()
    test_tree()
    test_place()
    return True
