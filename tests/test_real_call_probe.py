"""Consumer tests against shipped public predicates, without replacement."""

import io
import sys
import unittest
from collections.abc import Generator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from types import FrameType
from typing import cast

from real_call_probe import TraceHook, probe_calls

from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_tcin import is_target_tcin


@contextmanager
def prior_trace() -> Generator[TraceHook, None, None]:
    """Keep test failures and restoration mutants isolated from the runner."""
    original = cast("TraceHook | None", sys.gettrace())

    def prior(_frame: FrameType, _event: str, _argument: object) -> TraceHook:
        return prior

    try:
        sys.settrace(prior)
        yield prior
    finally:
        sys.settrace(original)


class RealCallProbeTests(unittest.TestCase):
    def test_real_predicate_results_and_events(self) -> None:
        for value, expected in (("12345678", True), ("1234567\n", False)):
            with self.subTest(value=value), prior_trace() as prior:
                events: list[str] = []
                result = probe_calls(
                    lambda value=value: is_target_tcin(value),
                    is_target_tcin.__code__,
                    events,
                )
                self.assertIs(result, expected)
                self.assertEqual(events, ["call"])
                self.assertIs(sys.gettrace(), prior)

    def test_real_guard_results_and_fixtures(self) -> None:
        native: dict[str, object] = {
            "items": [None, True, 7, 1.5, "text", {"nested": []}]
        }
        shared: list[object] = [1]
        alias: dict[str, object] = {"left": shared, "right": shared}
        for document, expected in ((native, True), (alias, False)):
            with self.subTest(expected=expected), prior_trace() as prior:
                events: list[str] = []
                result = probe_calls(
                    lambda document=document: is_bounded_json_tree(document),
                    is_bounded_json_tree.__code__,
                    events,
                )
                self.assertIs(result, expected)
                self.assertEqual(events, ["call"])
                self.assertIs(sys.gettrace(), prior)
        self.assertEqual(
            native, {"items": [None, True, 7, 1.5, "text", {"nested": []}]}
        )
        self.assertEqual(shared, [1])
        self.assertIs(alias["left"], shared)
        self.assertIs(alias["right"], shared)

    def test_restore_success(self) -> None:
        with prior_trace() as prior:
            events: list[str] = []
            result = probe_calls(
                lambda: is_target_tcin("12345678"),
                is_target_tcin.__code__,
                events,
            )
            self.assertIs(sys.gettrace(), prior)
            self.assertIs(result, True)
            self.assertEqual(events, ["call"])

    def test_injected_exceptions_restore_and_recover(self) -> None:
        failures: tuple[type[BaseException], ...] = (
            RuntimeError,
            KeyboardInterrupt,
            SystemExit,
        )
        for failure in failures:
            with self.subTest(failure=failure.__name__), prior_trace() as prior:
                events: list[str] = []
                with self.assertRaises(failure) as caught:
                    probe_calls(
                        lambda: is_target_tcin("12345678"),
                        is_target_tcin.__code__,
                        events,
                        failure,
                    )
                self.assertIs(type(caught.exception), failure)
                self.assertEqual(caught.exception.args, ())
                self.assertEqual(events, ["call"])
                self.assertIs(sys.gettrace(), prior)
                recovery_events: list[str] = []
                recovered = probe_calls(
                    lambda: is_target_tcin("12345678"),
                    is_target_tcin.__code__,
                    recovery_events,
                )
                self.assertIs(recovered, True)
                self.assertEqual(recovery_events, ["call"])
                self.assertIs(sys.gettrace(), prior)

    def test_operation_exception_identity_before_target(self) -> None:
        error = RuntimeError("before target")

        def operation() -> bool:
            raise error

        with prior_trace() as prior:
            events: list[str] = []
            with self.assertRaises(RuntimeError) as caught:
                probe_calls(operation, is_target_tcin.__code__, events)
            self.assertIs(caught.exception, error)
            self.assertEqual(events, [])
            self.assertIs(sys.gettrace(), prior)

    def test_unrelated_real_target_is_not_injected(self) -> None:
        with prior_trace() as prior:
            events: list[str] = []
            result = probe_calls(
                lambda: is_bounded_json_tree({"native": [None, True, 3]}),
                is_target_tcin.__code__,
                events,
                RuntimeError,
            )
            self.assertIs(result, True)
            self.assertEqual(events, [])
            self.assertIs(sys.gettrace(), prior)

    def test_empty_operation_restores(self) -> None:
        with prior_trace() as prior:
            events: list[str] = []
            result = probe_calls(lambda: None, is_target_tcin.__code__, events)
            self.assertIsNone(result)
            self.assertEqual(events, [])
            self.assertIs(sys.gettrace(), prior)

    def test_operation_side_effects_once(self) -> None:
        observations: list[str] = []

        def operation() -> bool:
            observations.append("before")
            result = is_target_tcin("12345678")
            observations.append("after")
            return result

        with prior_trace() as prior:
            events = ["existing"]
            result = probe_calls(operation, is_target_tcin.__code__, events)
            self.assertEqual(observations, ["before", "after"])
            self.assertIs(result, True)
            self.assertEqual(events, ["existing", "call"])
            self.assertIs(sys.gettrace(), prior)

    def test_exact_operation_result_identity(self) -> None:
        record: dict[str, object] = {"value": [1, None, "kept"]}
        guard_results: list[bool] = []

        def operation() -> dict[str, object]:
            guard_results.append(is_bounded_json_tree(record))
            return record

        with prior_trace() as prior:
            events: list[str] = []
            result = probe_calls(operation, is_bounded_json_tree.__code__, events)
            self.assertIs(result, record)
            self.assertEqual(record, {"value": [1, None, "kept"]})
            self.assertEqual(guard_results, [True])
            self.assertEqual(events, ["call"])
            self.assertIs(sys.gettrace(), prior)

    def test_no_output_for_success_or_injection(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with prior_trace() as prior, redirect_stdout(stdout), redirect_stderr(stderr):
            success_events: list[str] = []
            result = probe_calls(
                lambda: is_target_tcin("12345678"),
                is_target_tcin.__code__,
                success_events,
            )
            failure_events: list[str] = []
            with self.assertRaises(RuntimeError) as caught:
                probe_calls(
                    lambda: is_target_tcin("12345678"),
                    is_target_tcin.__code__,
                    failure_events,
                    RuntimeError,
                )
            self.assertIs(type(caught.exception), RuntimeError)
            self.assertIs(result, True)
            self.assertEqual(success_events, ["call"])
            self.assertEqual(failure_events, ["call"])
            self.assertIs(sys.gettrace(), prior)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
