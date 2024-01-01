#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Callable

from pyspartaproj.context.default.string_context import Strs
from pyspartaproj.script.decimal.initialize_decimal import initialize_decimal
from pyspartaproj.script.string.format_texts import format_indent
from pyspartaproj.script.time.count.count_elapsed import LogTimer

initialize_decimal()


def _stdout_check(
    expected: str,
    count: int,
    restart: Callable[[LogTimer], None],
    show: Callable[[LogTimer, int], str | None],
) -> None:
    timer = LogTimer()
    restart(timer)

    results: Strs = []

    for i in range(count):
        if time_text := show(timer, i):
            results += [time_text]

        timer.increase_timer()

    assert format_indent(expected) == "\n".join(results)


def test_count() -> None:
    expected: str = """
        1.0s
        2.0s
        3.0s
        4.0s
        5.0s
        6.0s
        7.0s
        8.0s
        9.0s
    """

    increase_count: int = 20

    def restart_timer(timer: LogTimer) -> None:
        timer.restart(override=True)

    def show_timer(timer: LogTimer, index: int) -> str | None:
        return timer.get_readable_time()

    _stdout_check(expected, increase_count, restart_timer, show_timer)


def test_interval() -> None:
    expected: str = """
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


def test_force() -> None:
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
            override=True, timer_interval=timer_interval, interval=interval
        )

    def show_timer(timer: LogTimer, index: int) -> str | None:
        result: str = f"i={index}"

        if time_text := timer.get_readable_time(force=True):
            result += ", " + time_text

        return result

    _stdout_check(expected, increase_count, restart_timer, show_timer)


def main() -> bool:
    test_count()
    test_interval()
    test_force()
    return True
