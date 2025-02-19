#!/usr/bin/env python

from pyspartalib.script.inherit.inherit_with import InheritWith
from pyspartalib.script.stdout.send_stdout import send_stdout


class TemporaryWith(InheritWith):
    def exit(self) -> None:
        send_stdout("exit")

    def __init__(self) -> None:
        send_stdout("init")
