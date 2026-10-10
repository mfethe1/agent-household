"""Synthetic fixtures only: no retailer or household qualification."""

import contextlib
import copy
import io
import sys
import threading
import unittest
from collections.abc import Iterator
from types import CodeType, FunctionType
from typing import NoReturn, cast

from real_call_probe import probe_calls

from agent_household.json_tree import is_bounded_json_tree

_CALLS: list[str] = []


class Hostile:
    def __str__(self) -> str:
        return self._fail("str")

    def __repr__(self) -> str:
        return self._fail("repr")

    def __iter__(self) -> Iterator[object]:
        return self._fail("iter")

    @staticmethod
    def _fail(name: str) -> NoReturn:
        _CALLS.append(name)
        raise AssertionError("synthetic callback invoked")


class ListSubclass(Hostile, list[object]):
    pass


class DictSubclass(Hostile, dict[str, object]):
    pass


class StringSubclass(Hostile, str):
    pass


class IntSubclass(int):
    pass


class FloatSubclass(float):
    pass


def chain(edges: int, shape: str, leaf: object = None) -> dict[str, object]:
    for index in range(edges - 1):
        leaf = (
            {"": leaf}
            if shape == "dict" or (shape == "mixed" and index % 2)
            else [leaf]
        )
    return {"": leaf}


def nodes(total: int, shape: str) -> dict[str, object]:
    if shape == "dict":
        return {str(index): None for index in range(total - 1)}
    if shape == "list":
        return {"": [None] * (total - 2)}
    return {"a": [None] * (total - 4), "b": {"c": None}}


def walk_code() -> CodeType:
    """The traversal the shipped guard calls inside its try, via its own globals."""
    bindings = cast("dict[str, object]", is_bounded_json_tree.__globals__)
    return cast("FunctionType", bindings["_walk"]).__code__


class JsonTreeTests(unittest.TestCase):
    def probe_walk(self, failure: type[BaseException]) -> tuple[bool, str]:
        """Raise `failure()` as traversal starts; return result and captured output."""
        document: dict[str, object] = {"a": [1]}
        previous = sys.gettrace()
        events: list[str] = []
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = probe_calls(
                    lambda: is_bounded_json_tree(document), walk_code(), events, failure
                )
        finally:
            self.assertEqual(events, ["call"])
            self.assertIs(sys.gettrace(), previous)
            self.assertEqual(document, {"a": [1]})
            self.assertIs(is_bounded_json_tree(document), True)
        return result, stdout.getvalue() + stderr.getvalue()

    def test_traversal_exceptions_fail_closed(self) -> None:
        for failure in (RuntimeError, MemoryError):
            with self.subTest(failure=failure.__name__):
                self.assertEqual(self.probe_walk(failure), (False, ""))

    def test_traversal_cancellation_propagates(self) -> None:
        for failure in (KeyboardInterrupt, SystemExit):
            with self.subTest(failure=failure.__name__):
                with self.assertRaises(failure) as caught:
                    self.probe_walk(failure)
                self.assertIs(type(caught.exception), failure)
                self.assertEqual(caught.exception.args, ())

    def test_roots_and_all_native_values(self) -> None:
        valid: list[object] = [{}, {"": [None, True, False, 0, -1, 1.5, "", {}, []]}]
        for value in valid:
            self.assertIs(is_bounded_json_tree(value), True)
        invalid: list[object] = [
            None,
            True,
            False,
            1,
            1.5,
            "",
            [],
            (),
            set(),
            b"",
            DictSubclass(),
        ]
        for value in invalid:
            self.assertIs(is_bounded_json_tree(value), False)

    def test_exact_types_and_callbacks_not_invoked(self) -> None:
        _CALLS.clear()
        bad: list[object] = [
            Hostile(),
            ListSubclass(),
            DictSubclass(),
            StringSubclass("x"),
            IntSubclass(1),
            FloatSubclass(1),
            (1,),
            {1},
            b"x",
        ]
        for value in bad:
            self.assertIs(is_bounded_json_tree({"x": value}), False)
            self.assertIs(is_bounded_json_tree(value), False)
        for key in (1, True, None, StringSubclass("x")):
            self.assertIs(is_bounded_json_tree({key: None}), False)
        self.assertEqual(_CALLS, [])

    def test_floats_and_integer_limits(self) -> None:
        bound = 10**4096
        for value in (0, 1, -1, bound - 1, -bound + 1, True, False):
            self.assertIs(is_bounded_json_tree({"": value}), True)
        for value in (bound, -bound, 1 << 100_000, -(1 << 100_000)):
            self.assertIs(is_bounded_json_tree({"": value}), False)
        for value in (0.0, -0.0, 1.7976931348623157e308, -1.7976931348623157e308):
            self.assertIs(is_bounded_json_tree({"": value}), True)
        for value in (float("nan"), float("inf"), -float("inf")):
            self.assertIs(is_bounded_json_tree({"": value}), False)

    def test_integer_limits_without_decimal_conversion(self) -> None:
        bound = 10**4096
        digits = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(640)
        try:
            accepted = [is_bounded_json_tree({"": n}) for n in (bound - 1, 1 - bound)]
            rejected = [is_bounded_json_tree({"": n}) for n in (bound, -bound)]
        finally:
            sys.set_int_max_str_digits(digits)
        self.assertEqual(accepted, [True, True])
        self.assertEqual(rejected, [False, False])

    def test_depth_all_layouts(self) -> None:
        for shape in ("dict", "list", "mixed"):
            for edges in (31, 32, 33):
                with self.subTest(shape=shape, edges=edges):
                    self.assertIs(
                        is_bounded_json_tree(chain(edges, shape)), edges <= 32
                    )

    def test_depth_empty_container_leaves(self) -> None:
        for shape in ("dict", "list", "mixed"):
            for leaf in ("list", "dict"):
                for edges in (32, 33):
                    with self.subTest(shape=shape, leaf=leaf, edges=edges):
                        document = chain(edges, shape, [] if leaf == "list" else {})
                        self.assertIs(is_bounded_json_tree(document), edges <= 32)

    def test_nodes_all_layouts_and_keys_excluded(self) -> None:
        for shape in ("dict", "list", "mixed"):
            for total in (9999, 10_000, 10_001):
                with self.subTest(shape=shape, total=total):
                    self.assertIs(
                        is_bounded_json_tree(nodes(total, shape)), total <= 10_000
                    )

    def test_aggregate_codepoint_boundaries(self) -> None:
        for total in (1_999_999, 2_000_000, 2_000_001):
            cases = [
                {"k": "x" * (total - 1)},
                {"k" * 1_000_000: "v" * (total - 1_000_000)},
                {"a": ["x" * 999_999, {"b": "y" * (total - 1_000_001)}]},
                {"k": "\U0001f642" * (total - 1)},
                {"k" * total: None},
            ]
            for index, document in enumerate(cases):
                with self.subTest(total=total, layout=index):
                    self.assertIs(is_bounded_json_tree(document), total <= 2_000_000)
        self.assertIs(is_bounded_json_tree({"": "x" * 2_000_001}), False)

    def test_equal_containers_aliases_and_scalar_occurrences(self) -> None:
        pairs: list[tuple[object, object]] = [
            ({}, {}),
            ([], []),
            ({"x": []}, {"x": []}),
        ]
        for a, b in pairs:
            self.assertIsNot(a, b)
            self.assertIs(is_bounded_json_tree({"a": a, "b": b}), True)
        shared_values: list[object] = [{}, []]
        for shared in shared_values:
            self.assertIs(is_bounded_json_tree({"a": shared, "b": shared}), False)
        scalar = "same scalar"
        self.assertIs(is_bounded_json_tree({"": [scalar, scalar]}), True)
        self.assertIs(is_bounded_json_tree({"": [scalar] * 9998}), True)
        self.assertIs(is_bounded_json_tree({"": [scalar] * 9999}), False)

    def test_cycles_and_identity_preserved(self) -> None:
        mapping: dict[str, object] = {}
        mapping["self"] = mapping
        sequence: list[object] = []
        sequence.append(sequence)
        nested: dict[str, object] = {"child": []}
        child: list[object] = [nested]
        nested["child"] = child
        for document in (mapping, {"list": sequence}, nested):
            self.assertIs(is_bounded_json_tree(document), False)
        self.assertIs(mapping["self"], mapping)
        self.assertIs(sequence[0], sequence)
        self.assertIs(nested["child"], child)
        self.assertIs(child[0], nested)

    def test_valid_invalid_nonmutation_and_no_output(self) -> None:
        sentinel = "SYNTHETIC_METADATA_SENTINEL"
        fixtures: list[dict[str, object]] = [
            {"meta": sentinel, "nested": [None, {"x": True}]},
            {"meta": sentinel, "bad": (1, 2)},
            {"meta": sentinel, "bad": float("inf")},
        ]
        for index, document in enumerate(fixtures):
            original = copy.deepcopy(document)
            identity = id(document)
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = is_bounded_json_tree(document)
            self.assertIs(result, index == 0)
            self.assertEqual(id(document), identity)
            self.assertEqual(document, original)
            self.assertNotIn(sentinel, repr(result))
            self.assertEqual(stdout.getvalue() + stderr.getvalue(), "")
        _CALLS.clear()
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = is_bounded_json_tree({"meta": sentinel, "bad": Hostile()})
        self.assertIs(result, False)
        self.assertEqual(_CALLS, [])
        self.assertNotIn(sentinel, repr(result))
        self.assertEqual(stdout.getvalue() + stderr.getvalue(), "")

    def test_native_concurrent_mutation_no_snapshot_claim(self) -> None:
        document: dict[str, object] = {str(index): None for index in range(9999)}
        started, stop = threading.Event(), threading.Event()

        def mutate() -> None:
            started.set()
            while not stop.is_set():
                document["changing"] = None
                _ = document.pop("changing", None)

        worker = threading.Thread(target=mutate)
        worker.start()
        try:
            self.assertTrue(started.wait(2))
            for _ in range(40):
                self.assertIs(type(is_bounded_json_tree(document)), bool)
        finally:
            stop.set()
            worker.join(2)
        self.assertFalse(worker.is_alive())
