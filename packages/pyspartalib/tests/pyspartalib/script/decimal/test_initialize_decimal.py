#!/usr/bin/env python

"""Test module to help calculating by Decimal type."""

from decimal import Context, Decimal, FloatOperation, getcontext, setcontext

from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.decimal.initialize_decimal import initialize_decimal
from tests.pyspartalib.interface.pytest import raises


def test_float() -> None:
    """Test for assign float to Decimal type directly."""
    with raises(FloatOperation):
        initialize_decimal()
        Decimal(1.0)


def test_accuracy() -> None:
    """Test for accuracy of calculating Decimal type."""

    def get_changed() -> Strs:
        context = getcontext()
        return [str(context.prec), context.rounding]

    setcontext(Context())
    before: Strs = get_changed()

    initialize_decimal()
    after: Strs = get_changed()

    if before == after:
        raise ValueError
