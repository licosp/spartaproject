#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from platform import uname

from pyspartaproj.context.default.string_context import StrGene, Strs
from pyspartaproj.script.file.json.project_context import ProjectContext
from pyspartaproj.script.shell.execute_command import execute_command


def _get_powershell_path() -> str:
    project = ProjectContext()
    return project.get_path_context("runtime")[
        project.get_platform_key(["powershell"]) + ".path"
    ].as_posix()


def execute_powershell(commands: Strs) -> StrGene:
    shell_commands: Strs = [
        _get_powershell_path(),
        "-ExecutionPolicy",
        "Bypass",
    ] + commands

    return execute_command(shell_commands)


def get_path_string(path: Path) -> str:
    path_text: str = str(path)

    if "Linux" == uname().system:
        return path_text.replace("/", "\\")

    return path_text


def get_quoted_paths(path: Path) -> str:
    return get_path_string(path).join(["'"] * 2)


def get_script_executable(commands_execute: Strs) -> str:
    return " ".join(commands_execute).join(['"'] * 2)
