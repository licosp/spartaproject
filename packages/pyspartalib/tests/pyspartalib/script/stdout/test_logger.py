#!/usr/bin/env python

from pyspartalib.context.callable_context import Type


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError
