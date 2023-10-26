#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to execute Python according to OS."""

from pathlib import Path

from pyspartaproj.context.default.string_context import StrGene, Strs
from pyspartaproj.script.project.project_context import ProjectContext
from pyspartaproj.script.shell.execute_command import execute_command


def get_interpreter_path() -> Path:
    """Function to get interpreter path of Python according to OS.

    Raises:
        FileNotFoundError: raise error when selected platform isn't defined

    Returns:
        Path: relative path of Python interpreter
    """
    project = ProjectContext()
    return project.merge_platform_path("filter", "platform", "interpreter")


def execute_python(commands: Strs) -> StrGene:
    """Execute Python according to OS.

    Args:
        commands (Strs): Script you want execute and arguments of itself

    Returns:
        StrGene: Stdout of Script path you want execute
    """
    return execute_command([get_interpreter_path().as_posix()] + commands)
