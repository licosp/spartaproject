#!/usr/bin/env python

from pyspartalib.context.custom.type_context import Type
from pyspartalib.script.project.log_pipeline import LogPipeline
from pyspartalib.script.project.walk_pipeline import WalkPipeline
from pyspartalib.script.stdout.send_stdout import send_stdout


class LaunchTest(WalkPipeline):
    def __initialize_super_class(self) -> None:
        super().__init__(True)

    def launch_pipeline(self) -> None:
        send_stdout("launch")

    def __init__(self) -> None:
        self.__initialize_super_class()


def _difference_error(result: Type, expected: Type) -> None:
    if result != expected:
        raise ValueError


def _get_expected_launch() -> str:
    return """
        0.0s: begin
        launch
        0.0s: end
    """


def _restart_timer(pipeline: LogPipeline) -> None:
    pipeline.restart(override=True)


def _edit_pipeline_launch() -> None:
    pipeline = LaunchTest()
    _restart_timer(pipeline)
    pipeline.initialize_pipeline()
