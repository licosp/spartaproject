#!/usr/bin/env python

"""Module to show Python system paths."""

from sys import path


def _main() -> None:
    for text in path:
        print(text)


if __name__ == "__main__":
    _main()
