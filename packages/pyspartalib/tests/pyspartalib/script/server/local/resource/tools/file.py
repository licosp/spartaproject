#!/usr/bin/env python

"""Script to execute Python module from file tree on server."""


def _main() -> None:
    for i in range(3):
        print("file" + str(i))


if __name__ == "__main__":
    _main()
