"""Single-record consumer assertions; not module or whole-page acceptance."""

import ast
import copy
import inspect
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from typing import cast

from hostile_callbacks import (
    CALLBACK_NAMES,
    CallbackCounts,
    HostileDict,
    HostileList,
    HostileString,
)
from hostile_callbacks import (
    HostileObject as Hostile,
)
from real_call_probe import TraceHook, probe_calls

from agent_household import target_record_title
from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_record_title import collect_record_title
from agent_household.target_tcin import is_target_tcin

ID = "12345678"


def fixture(tcin: object = ID, title: object = "raw") -> dict[str, object]:
    return {"tcin": tcin, "title": title}


def counters() -> CallbackCounts:
    return dict.fromkeys(CALLBACK_NAMES, 0)


class RecordTitleTests(unittest.TestCase):
    def fact(self, record: object, expected: object, result: tuple[str, ...]) -> None:
        actual = collect_record_title(record, expected)
        self.assertEqual(actual, result)
        self.assertIs(type(actual), tuple)
        for value in cast("tuple[str, ...]", actual):
            self.assertIs(type(value), str)

    def test_r01_facts_and_raw_strings(self) -> None:
        self.fact(fixture(), ID, ("raw",))
        self.fact(fixture("00001234"), "00001234", ("raw",))
        self.fact({"title": "ignored"}, ID, ())
        self.fact(fixture("87654321"), ID, ())
        titles = ("", "&amp;&#65;", " \t\nraw\r ", "\0", "\u0627", "\uff11", "\ud800")
        for index, title in enumerate(titles):
            with self.subTest(raw=index):
                self.fact(fixture(title=title), ID, (title,))
        for index, tcin in enumerate(("", "x" * 100, "\u0627", "\uff11", "\ud800")):
            with self.subTest(nonmatching=index):
                self.fact(fixture(tcin, {"ignored": [None]}), ID, ())

    def test_r02_native_type_matrix(self) -> None:
        rows: tuple[tuple[str, object], ...] = (
            ("null", None),
            ("bool", True),
            ("int", 1),
            ("float", 1.5),
            ("list", []),
            ("dict", {}),
        )
        for name, value in rows:
            with self.subTest(present_tcin=name):
                self.assertIsNone(collect_record_title(fixture(value), ID))
            with self.subTest(matching_title=name):
                self.assertIsNone(
                    collect_record_title(fixture(title=copy.deepcopy(value)), ID)
                )
            with self.subTest(ignored_title=name):
                self.fact(fixture("other", copy.deepcopy(value)), ID, ())
        with self.subTest(missing_title="matching"):
            self.assertIsNone(collect_record_title({"tcin": ID}, ID))
        with self.subTest(missing_title="nonmatching"):
            self.fact({"tcin": "other"}, ID, ())

    def test_r03_invalid_ids_and_hostile_callbacks(self) -> None:
        counts = counters()
        hostile_record = HostileDict(counts)
        invalid: tuple[object, ...] = (
            "",
            "1234567",
            "123456789",
            "1234567x",
            "1234567\n",
            "\u0661" * 8,
            "\uff11" * 8,
            True,
            None,
            12345678,
            HostileString(ID, counts),
            Hostile(counts),
        )
        for index, expected in enumerate(invalid):
            with self.subTest(invalid_id=index):
                self.assertIsNone(collect_record_title(hostile_record, expected))
                native = fixture()
                before = copy.deepcopy(native)
                self.assertIsNone(collect_record_title(native, expected))
                self.assertEqual(native, before)
        self.assertIsNone(collect_record_title(fixture("bad"), "bad"))
        self.fact(fixture("00001234"), "00001234", ("raw",))
        hostile_values: tuple[object, ...] = (
            Hostile(counts),
            HostileString(ID, counts),
            HostileDict(counts),
            HostileList(counts),
        )
        for index, value in enumerate(hostile_values):
            with self.subTest(hostile_value=index):
                self.assertIsNone(collect_record_title(value, ID))
                self.assertIsNone(collect_record_title(fixture(value), ID))
                self.assertIsNone(collect_record_title(fixture(title=value), ID))
                self.assertIsNone(collect_record_title({"metadata": value}, ID))
        self.assertEqual(counts, counters())

    def pair(self, name: str, rejected: object, control: object) -> None:
        with self.subTest(guard_pair=name):
            self.assertTrue(is_bounded_json_tree(control))
            self.fact(control, ID, ("raw",))
            self.assertFalse(is_bounded_json_tree(rejected))
            self.assertIsNone(collect_record_title(rejected, ID))

    def test_r04_guard_rejection_control_pairs(self) -> None:
        for index, root in enumerate((None, [], "record", True, 1)):
            self.pair(f"root-{index}", root, fixture())
        counts = counters()
        for name, descendant in (
            ("string", HostileString("metadata", counts)),
            ("dict", HostileDict(counts)),
            ("list", HostileList(counts)),
        ):
            rejected = fixture()
            rejected["metadata"] = descendant
            control = fixture()
            control["metadata"] = "native"
            self.pair(f"subclass-{name}", rejected, control)
        self.pair("subclass-root", HostileDict(counts), fixture())
        self.assertEqual(counts, counters())
        cycle = fixture()
        cycle["metadata"] = cycle
        self.pair("cycle", cycle, fixture())
        shared: list[object] = []
        alias = fixture()
        alias["metadata"] = [shared, shared]
        independent = fixture()
        independent["metadata"] = [[], []]
        self.pair("alias", alias, independent)
        for index, number in enumerate((float("nan"), float("inf"), -float("inf"))):
            rejected = fixture()
            rejected["metadata"] = number
            control = fixture()
            control["metadata"] = 1.5
            self.pair(f"nonfinite-{index}", rejected, control)
        rejected = fixture()
        rejected["metadata"] = 10**4096
        control = fixture()
        control["metadata"] = 10**4096 - 1
        self.pair("integer-boundary", rejected, control)
        text_control = fixture()
        text_control["metadata"] = ""
        total = sum(len(key) for key in text_control) + len(ID) + len("raw")
        self.assertEqual(total, 28)
        text_control["metadata"] = "x" * (2_000_000 - total)
        text_rejected = text_control.copy()
        text_rejected["metadata"] = "x" * (2_000_000 - total + 1)
        self.pair("total-text-boundary", text_rejected, text_control)

    def test_r05_silence_ownership_and_immutable_result(self) -> None:
        metadata: dict[str, object] = {"sentinel": ["not a title"]}
        record = fixture()
        record["metadata"] = metadata
        record["sibling"] = "never surfaced"
        before = copy.deepcopy(record)
        identities = (id(record), id(metadata), id(metadata["sentinel"]))
        rejected = fixture(title=None)
        rejected_before = copy.deepcopy(rejected)
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = collect_record_title(record, ID)
            self.assertIsNone(collect_record_title(rejected, ID))
            self.assertIsNone(collect_record_title(record, "invalid"))
        self.assertEqual((stdout.getvalue(), stderr.getvalue()), ("", ""))
        self.assertEqual(record, before)
        self.assertEqual(rejected, rejected_before)
        self.assertEqual(
            identities, (id(record), id(metadata), id(metadata["sentinel"]))
        )
        self.assertEqual(result, ("raw",))
        self.assertIs(type(result), tuple)
        values = cast("tuple[str, ...]", result)
        self.assertIs(type(values[0]), str)
        with self.assertRaises(TypeError):
            operator_target = cast("list[str]", values)
            operator_target[0] = "replacement"
        self.assertEqual(record, before)

    def test_r06_real_guard_calls_and_trace_cleanup(self) -> None:
        previous = cast("TraceHook | None", sys.gettrace())
        events: list[str] = []
        counts = counters()
        try:
            for expected in ("invalid", None, HostileString(ID, counts)):
                events.clear()
                self.assertIsNone(
                    probe_calls(
                        lambda expected=expected: collect_record_title(
                            HostileDict(counts), expected
                        ),
                        is_bounded_json_tree.__code__,
                        events,
                    )
                )
                self.assertEqual(events, [])
                self.assertIs(sys.gettrace(), previous)
            events.clear()
            self.assertEqual(
                probe_calls(
                    lambda: collect_record_title(fixture(), ID),
                    is_bounded_json_tree.__code__,
                    events,
                ),
                ("raw",),
            )
            self.assertEqual(events, ["call"])
            for failure in (RuntimeError, KeyboardInterrupt, SystemExit):
                with self.subTest(failure=failure.__name__):
                    events.clear()
                    if failure is RuntimeError:
                        self.assertIsNone(
                            probe_calls(
                                lambda: collect_record_title(fixture(), ID),
                                is_bounded_json_tree.__code__,
                                events,
                                failure,
                            )
                        )
                    else:
                        with self.assertRaises(failure):
                            probe_calls(
                                lambda: collect_record_title(fixture(), ID),
                                is_bounded_json_tree.__code__,
                                events,
                                failure,
                            )
                    self.assertEqual(events, ["call"])
                    self.assertIs(sys.gettrace(), previous)
                    events.clear()
                    self.assertEqual(
                        probe_calls(
                            lambda: collect_record_title(fixture(), ID),
                            is_bounded_json_tree.__code__,
                            events,
                        ),
                        ("raw",),
                    )
                    self.assertEqual(events, ["call"])
                    self.assertIs(sys.gettrace(), previous)
            self.assertEqual(counts, counters())
        finally:
            sys.settrace(previous)
        self.assertIs(sys.gettrace(), previous)

    def test_r07_direct_dependency_wiring(self) -> None:
        source = inspect.getsource(target_record_title)
        tree = ast.parse(source)
        required = {
            "is_target_tcin": ("agent_household.target_tcin", is_target_tcin),
            "is_bounded_json_tree": (
                "agent_household.json_tree",
                is_bounded_json_tree,
            ),
        }
        functions = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "collect_record_title"
        ]
        self.assertEqual(len(functions), 1)
        function = functions[0]
        globals_map = cast("dict[str, object]", collect_record_title.__globals__)
        self.assertIs(collect_record_title, target_record_title.collect_record_title)
        self.assertIs(globals_map, vars(target_record_title))
        for binding, (module_name, dependency) in required.items():
            with self.subTest(binding=binding):
                self.assertIs(getattr(target_record_title, binding), dependency)
                self.assertIs(globals_map[binding], dependency)
                imports = [
                    alias.asname or alias.name
                    for node in tree.body
                    if isinstance(node, ast.ImportFrom) and node.module == module_name
                    for alias in node.names
                    if alias.name == binding
                ]
                self.assertEqual(imports, [binding])
                calls = [
                    node
                    for node in ast.walk(function)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == binding
                ]
                self.assertEqual(len(calls), 1)
                for node in ast.walk(function):
                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                        self.assertNotEqual(node.id, binding)
                    if isinstance(node, ast.arg):
                        self.assertNotEqual(node.arg, binding)
                    if isinstance(
                        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                    ):
                        self.assertNotEqual(node.name, binding)
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        for alias in node.names:
                            self.assertNotEqual(
                                alias.asname or alias.name.split(".")[0], binding
                            )
                    if isinstance(node, ast.ExceptHandler):
                        self.assertNotEqual(node.name, binding)
