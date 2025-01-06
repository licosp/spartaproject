#!/usr/bin/env python

"""Test module to redirect stdout to string variable forcibly."""

from pyspartalib.script.stdout.logger import show_log
from pyspartalib.script.stdout.off_stdout import StdoutText
from pyspartalib.script.string.format_texts import format_indent


def test_messages() -> None:
    """Test to redirect stdout to string variable forcibly."""
    message: str = "Hello, World!"
    expected: str = """
        Hello, World!
        Hello, World!
        """

    stdout_text = StdoutText()

    @stdout_text.decorator
    def _messages() -> None:
        show_log(message)
        show_log(message)

    _messages()

    assert format_indent(expected, stdout=True) == stdout_text.show()
