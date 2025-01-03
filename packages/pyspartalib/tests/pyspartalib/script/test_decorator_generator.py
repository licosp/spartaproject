#!/usr/bin/env python

from typing import Callable

from pyspartalib.context.callable_context import CP, CR
from pyspartalib.script.decorator_generator import TransferFunction


class TemporaryDecorator(TransferFunction):
    def __init__(self, text: str | None = None) -> None:
        if text is None:
            text = ""

        self.text = text

    def wrapper(
        self,
        function: Callable[CP, CR],
        *arguments: CP.args,
        **key_arguments: CP.kwargs,
    ) -> CR:
        result: CR = function(*arguments, **key_arguments)
        self.text *= 2
        return result

    def show(self) -> str:
        return self.text


def test_name() -> None:
    test_instance = TemporaryDecorator()

    @test_instance.decorator
    def text_print() -> None:
        pass

    text_print()

    expected_function: str = "text_print"
    assert expected_function == text_print.__name__


def test_doc() -> None:
    test_instance = TemporaryDecorator()

    @test_instance.decorator
    def text_print() -> None:
        """Text doc."""
        pass

    text_print()

    expected_doc: str = "Text doc."
    assert expected_doc == text_print.__doc__


def test_text() -> None:
    message: str = "Hello!"
    test_instance = TemporaryDecorator(message)

    @test_instance.decorator
    def text_print() -> None:
        pass

    text_print()

    expected_text: str = "Hello!Hello!"
    assert expected_text == test_instance.show()
