#!/usr/bin/env python

"""Test module to handle I/O functionalities of any script called pipeline."""

from decimal import Decimal

from pyspartalib.context.custom.type_context import Type
from pyspartalib.context.default.string_context import Strs
from pyspartalib.script.pipeline.log_pipeline import LogPipeline
from pyspartalib.script.stdout.off_stdout import OffStdout
from tests.pyspartalib.script.pipeline.context.log_context import LogFunc


def _none_error(result: Type | None) -> Type:
    if result is None:
        raise ValueError

    return result


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_interval() -> Decimal:
    return Decimal("0.3")


def _get_interval_texts() -> Strs:
    return ["0.0"] + [str(_get_interval())] * 2


def _get_message() -> str:
    return "test"


def _get_messages() -> Strs:
    return [_get_message()]


def _get_message_texts() -> Strs:
    return ["begin", _get_message(), "end"]


def _get_timer_log(interval: str, messages: str) -> str:
    return interval + "s" + ": " + messages


def _get_expected_log() -> Strs:
    return [
        _get_timer_log(interval, message)
        for interval, message in zip(
            _get_interval_texts(),
            _get_message_texts(),
            strict=True,
        )
    ]


def _get_expected() -> str:
    return _get_timer_log(str(_get_interval()), _get_message())


def _get_expected_single() -> Strs:
    return [_get_expected()]


def _show_log(messages: Strs, pipeline: LogPipeline) -> LogPipeline:
    pipeline.show_log(messages, force=True)
    return pipeline


def _decorate_function(function: LogFunc, off_stdout: OffStdout) -> str:
    @off_stdout.decorator
    def _messages() -> None:
        function()

    _messages()

    return off_stdout.show()


def _execute_log_function(function: LogFunc) -> str:
    return _decorate_function(function, OffStdout())


def _initialize_pipeline(pipeline: LogPipeline) -> None:
    pipeline.restart(override=True, timer_interval=_get_interval())
    pipeline.increase_timer()


def _start_pipeline(function: LogFunc) -> LogPipeline:
    pipeline: LogPipeline = function()
    _initialize_pipeline(pipeline)
    return pipeline


def _record_log(function: LogFunc) -> LogPipeline:
    return _show_log(_get_messages(), _start_pipeline(function))


def _record_log_single(function: LogFunc) -> LogPipeline:
    return _show_log(
        _get_messages(),
        _reset_stored_log(_start_pipeline(function)),
    )


def _wrapper_print(function: LogFunc) -> LogFunc:
    return lambda: _record_log(function)


def _get_result_print(function: LogFunc) -> Strs:
    return _execute_log_function(_wrapper_print(function)).splitlines()


def _get_log(pipeline: LogPipeline) -> Strs:
    return _none_error(pipeline.get_log())


def _reset_stored_log(pipeline: LogPipeline) -> LogPipeline:
    _get_log(pipeline)
    return pipeline


def _close_log(pipeline: LogPipeline) -> Strs:
    return _none_error(pipeline.close_log())


def _get_result_all(function: LogFunc) -> Strs:
    return _close_log(_record_log(function))


def _get_result_single(function: LogFunc) -> Strs:
    return _get_log(_record_log_single(function))


def _create_pipeline() -> LogPipeline:
    return LogPipeline(enable_shown=True)


def _create_pipeline_text() -> LogPipeline:
    return LogPipeline()


def _compare_text(expected: Strs, result: Strs) -> None:
    _difference_error(result, expected)


def test_print() -> None:
    """Test to show log messages to stdout."""
    _compare_text(_get_expected_log(), _get_result_print(_create_pipeline))


def test_all() -> None:
    """Test to get log messages recorded in instance inside."""
    _compare_text(_get_expected_log(), _get_result_all(_create_pipeline_text))


def test_single() -> None:
    """Test to get log messages except automatically generated stuff."""
    _compare_text(
        _get_expected_single(),
        _get_result_single(_create_pipeline_text),
    )
