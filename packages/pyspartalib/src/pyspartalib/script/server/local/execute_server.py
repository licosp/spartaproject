#!/usr/bin/env python

"""Module to execute python code on server you can use ssh connection."""

from collections.abc import Sized
from pathlib import Path

from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.server.local.upload_server import UploadServer
from pyspartalib.script.server.script_version import get_version_name


class ExecuteServer(UploadServer):
    """Class to execute python code on server."""

    def __initialize_super_class(
        self,
        local_root: Path | None,
        override: bool,
        jst: bool,
        forward: Path | None,
        platform: str | None,
    ) -> None:
        super().__init__(
            local_root=local_root,
            override=override,
            jst=jst,
            forward=forward,
            platform=platform,
        )

    def _length_error(self, result: Sized, expected: int) -> None:
        if len(result) != expected:
            raise ValueError

    def _set_version(self, version: str | None) -> str:
        if version is None:
            version = "3.11.5"

        return get_version_name(version)

    def _get_runtime_path(self, runtime_root: Path, version: str) -> Path:
        return Path(runtime_root, version, "bin", "python3")

    def _get_filter_head(self) -> str:
        return "traceback".capitalize()

    def _error_strings(self) -> Strs:
        return ["most", "recent", "call", "last"]

    def _get_filter_inside(self) -> str:
        return " ".join(self._error_strings())

    def _get_filter_body(self) -> str:
        return "(" + self._get_filter_inside() + ")"

    def _get_error_identifier(self) -> str:
        return self._get_filter_head() + " " + self._get_filter_body() + ":"

    def __initialize_variables(self, version: str | None) -> None:
        self._runtime_path: Path = self._get_runtime_path(
            self.get_path("python_root"),
            self._set_version(version),
        )
        self._error_identifier: str = self._get_error_identifier()

    def _get_command(self, source_root: Path) -> Strs:
        return [
            path.as_posix()
            for path in [
                self._runtime_path,
                self.to_relative_path(source_root),
            ]
        ]

    def _execute_command(self, source_root: Path) -> Strs | None:
        return self.execute_ssh(self._get_command(source_root))

    def execute(self, source_root: Path) -> Strs | None:
        """Execute Python code you selected.

        Args:
            source_root (Path):
                Local path of Python code you will upload and execute.

        Returns:
            Strs | None:
                Stdout of executed Python code when execution is successful.

        """
        if not self.upload(source_root):
            return None

        if (result := self._execute_command(source_root)) is None:
            return None

        self._contain_error(self._error_identifier, result)

        return result

    def __init__(
        self,
        version: str | None = None,
        local_root: Path | None = None,
        override: bool = False,
        jst: bool = False,
        forward: Path | None = None,
        platform: str | None = None,
    ) -> None:
        """Select version of Python, then ready using ssh and sftp connection.

        Args:
            version (str | None, optional): Defaults to None.
                Version information of Python you want to execute.

            local_root (Path | None, optional): Defaults to None.
                User defined path of local working space which is used.
                It's used for argument "local_root" of class "UploadServer".

            override (bool, optional): Defaults to False.
                Override initial time count to "2023/4/1:12:00:00-00 (AM)".
                It's used for argument "override" of class "UploadServer".

            jst (bool, optional): Defaults to False.
                If True, you can get datetime object as JST time zone.
                It's used for argument "jst" of class "UploadServer".

            forward (Path | None, optional): Defaults to None.
                Path of setting file in order to place
                    project context file to any place.
                It's used for argument "forward" of class "UploadServer".

            platform (str | None, optional): Defaults to None.
                Platform information should be "linux" or "windows",
                    and it's used in the project context file like follow.
                It's used for argument "platform" of class "UploadServer".

        """
        self.__initialize_super_class(
            local_root,
            override,
            jst,
            forward,
            platform,
        )
        self.__initialize_variables(version)
