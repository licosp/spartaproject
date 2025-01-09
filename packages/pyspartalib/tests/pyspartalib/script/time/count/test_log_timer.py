#!/usr/bin/env python

"""Test module to count timer and get timer count by readable format."""

from decimal import Decimal

from pyspartalib.context.custom.timer_context import TimerFunc, TimerIntStrFunc
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.decimal.initialize_decimal import initialize_decimal
from pyspartalib.script.string.format_texts import format_indent
from pyspartalib.script.time.count.log_timer import LogTimer

initialize_decimal()


def _get_time_texts(
    count: int,
    show: TimerIntStrFunc,
    timer: LogTimer,
) -> Strs:
    results: Strs = []

    for i in range(count):
        if time_text := show(timer, i):
            results += [time_text]

        timer.increase_timer()

    return results


def _stdout_check(
    expected: str,
    count: int,
    restart: TimerFunc,
    show: TimerIntStrFunc,
) -> None:
    timer = LogTimer()
    restart(timer)

    results: Strs = _get_time_texts(count, show, timer)

    assert format_indent(expected) == "\n".join(results)


def _get_expected_count() -> str:
    return """
        1.0s
        2.0s
        3.0s
        4.0s
        5.0s
        6.0s
        7.0s
        8.0s
        9.0s
        10.0s
    """


def _get_expected_interval() -> str:
    return """
        30m 0.0s
        1h 0.0s
        1h 30m 0.0s
        2h 0.0s
        2h 30m 0.0s
        3h 0.0s
        3h 30m 0.0s
        4h 0.0s
        4h 30m 0.0s
        5h 0.0s
    """


def test_count() -> None:
    """Test to get timer count by readable format."""
    expected: str = _get_expected_count()
    increase_count: int = 20 + 1

    def restart_timer(timer: LogTimer) -> None:
        timer.restart(override=True)

    def show_timer(timer: LogTimer, _: int) -> str | None:
        return timer.get_readable_time()

    _stdout_check(expected, increase_count, restart_timer, show_timer)


def test_interval() -> None:
    """Test to get timer count with specific interval."""
    expected: str = _get_expected_interval()
    minutes: int = 60
    timer_interval: Decimal = Decimal(str(minutes * 10))
    interval: Decimal = Decimal(str(minutes * 30))

    increase_count: int = 30 + 1

    def restart_timer(timer: LogTimer) -> None:
        timer.restart(
            override=True,
            timer_interval=timer_interval,
            interval=interval,
        )

    def show_timer(timer: LogTimer, _: int) -> str | None:
        return timer.get_readable_time()

    _stdout_check(expected, increase_count, restart_timer, show_timer)


def test_digit() -> None:
    """Test to get timer count with digit of decimal point."""
    expected: str = """
        0.010s
        0.020s
        0.030s
        0.040s
        0.050s
        0.060s
        0.070s
        0.080s
        0.090s
        0.100s
    """

    interval: Decimal = Decimal(str(0.01))
    digit: int = 3

    increase_count: int = 10 + 1

    def restart_timer(timer: LogTimer) -> None:
        timer.restart(
            override=True,
            timer_interval=interval,
            interval=interval,
            digit=digit,
        )

    def show_timer(timer: LogTimer, _: int) -> str | None:
        return timer.get_readable_time()

    _stdout_check(expected, increase_count, restart_timer, show_timer)


def test_force() -> None:
    """Test to get timer count forcibly."""
    expected: str = """
        i=0, 0.0s
        i=1, 0.1s
        i=2, 0.2s
        i=3, 0.3s
        i=4, 0.4s
        i=5, 0.5s
        i=6, 0.6s
        i=7, 0.7s
        i=8, 0.8s
        i=9, 0.9s
    """

    timer_interval: Decimal = Decimal(str(0.1))
    interval: Decimal = Decimal(str(1.0))

    increase_count: int = 10

    def restart_timer(timer: LogTimer) -> None:
        timer.restart(
            override=True,
            timer_interval=timer_interval,
            interval=interval,
        )

    def show_timer(timer: LogTimer, index: int) -> str | None:
        result: str = f"i={index}"

        if time_text := timer.get_readable_time(force=True):
            result += ", " + time_text

        return result

    _stdout_check(expected, increase_count, restart_timer, show_timer)
