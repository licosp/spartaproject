#!/usr/bin/env python

"""Test module to upload file or directory by SFTP functionality."""

from pathlib import Path
from tempfile import TemporaryDirectory

from pyspartalib.context.extension.path_context import PathFunc
from pyspartalib.script.directory.create_directory import create_directory
from pyspartalib.script.path.modify.get_resource import get_resource
from pyspartalib.script.path.temporary.create_temporary_file import (
    create_temporary_file,
)
from pyspartalib.script.path.temporary.create_temporary_tree import (
    create_temporary_tree,
)
from pyspartalib.script.server.local.upload_server import UploadServer


def _fail_error(status: bool) -> None:
    if not status:
        raise ValueError


def _get_config_file() -> Path:
    return get_resource(local_path=Path("forward.json"))


def _upload_path(server: UploadServer, source_path: Path) -> None:
    _fail_error(server.upload(source_path))


def _upload_path_local(
    server: UploadServer,
    source_path: Path,
    destination_path: Path,
) -> None:
    _fail_error(server.upload(source_path, destination=destination_path))


def _is_connect(server: UploadServer) -> None:
    _fail_error(server.connect())


def _get_server() -> UploadServer:
    return UploadServer(jst=True, forward=_get_config_file())


def _get_server_local(local_root: Path) -> UploadServer:
    return UploadServer(
        jst=True,
        local_root=local_root,
        forward=_get_config_file(),
    )


def _inside_temporary_directory(function: PathFunc) -> None:
    with TemporaryDirectory() as temporary_path:
        function(Path(temporary_path))


def test_file() -> None:
    """Test to upload single file to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(server, create_temporary_file(server.get_date_time_root()))


def test_directory() -> None:
    """Test to upload single directory to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(
        server,
        create_directory(Path(server.get_date_time_root(), "directory")),
    )


def test_tree() -> None:
    """Test to upload multiple files and directories to server."""
    server: UploadServer = _get_server()
    _is_connect(server)

    _upload_path(
        server,
        create_temporary_tree(
            Path(server.get_date_time_root(), "tree"),
            tree_deep=2,
        ),
    )


def test_place() -> None:
    """Test to upload single file from selected local root to server."""

    def individual_test(temporary_root: Path) -> None:
        server: UploadServer = _get_server_local(temporary_root)
        _is_connect(server)

        source_path: Path = create_temporary_file(server.get_date_time_root())

        _upload_path_local(
            server,
            source_path,
            server.to_relative_path(source_path),
        )

    _inside_temporary_directory(individual_test)
