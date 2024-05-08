#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test module to use SSH and SFTP functionality."""

from pyspartaproj.interface.pytest import fail
from pyspartaproj.script.server.local.connect_server import ConnectServer


def _is_connect() -> ConnectServer:
    server = ConnectServer()

    if server.connect():
        return server

    fail()


def test_connect() -> None:
    """Test to connect server by using SSH and SFTP functionality."""
    _is_connect()


def main() -> bool:
    """Run all tests.

    Returns:
        bool: Success if get to the end of function.
    """
    test_connect()
    return True
