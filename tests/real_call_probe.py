"""Current-thread synchronous observation of a real Python function call."""

import sys
from collections.abc import Callable
from types import CodeType, FrameType
from typing import TypeAlias, TypeVar, cast

T = TypeVar("T")
TraceHook: TypeAlias = Callable[[FrameType, str, object], "TraceHook | None"]


def probe_calls(
    operation: Callable[[], T],
    target: CodeType,
    events: list[str],
    failure: type[BaseException] | None = None,
) -> T:
    """Observe target calls, optionally inject failure, and restore tracing."""
    previous = cast("TraceHook | None", sys.gettrace())

    def trace(frame: FrameType, event: str, _argument: object) -> TraceHook:
        if event == "call" and frame.f_code is target:
            events.append("call")
            if failure is not None:
                raise failure()
        return trace

    try:
        sys.settrace(trace)
        return operation()
    finally:
        sys.settrace(previous)
