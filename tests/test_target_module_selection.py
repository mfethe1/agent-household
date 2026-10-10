"""Named admission matrices with real guard tracing and binding evidence."""

import ast
import copy
import inspect
import io
import sys
import unittest
from collections.abc import Callable, Generator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from types import FrameType
from typing import cast

from hostile_callbacks import (
    CALLBACK_NAMES,
    CallbackCounts,
    HostileDict,
    HostileList,
    HostileObject,
    HostileString,
)
from real_call_probe import TraceHook, probe_calls

from agent_household import target_module_selection as selection
from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_tcin import is_target_tcin

TCIN = "01234567"
Factory = Callable[[], object]


def selected(**fields: object) -> dict[str, object]:
    return {
        "module_type": "ProductDetailTitle",
        "version": 0,
        "module_data": {"data_by_tcin": []},
        **fields,
    }


@contextmanager
def prior_trace() -> Generator[TraceHook, None, None]:
    original = cast("TraceHook | None", sys.gettrace())

    def prior(_frame: FrameType, _event: str, _arg: object) -> TraceHook:
        return prior

    try:
        sys.settrace(prior)
        yield prior
    finally:
        sys.settrace(original)


class SelectionTests(unittest.TestCase):
    def check(
        self,
        document: object,
        expected: bool | None,
        identifier: object = TCIN,
        calls: int = 1,
    ) -> None:
        out, err, events = io.StringIO(), io.StringIO(), cast("list[str]", [])
        with redirect_stdout(out), redirect_stderr(err):
            result = probe_calls(
                lambda: selection.is_title_module(document, identifier),
                is_bounded_json_tree.__code__,
                events,
            )
        self.assertIs(result, expected)
        self.assertEqual(events, ["call"] * calls)
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))

    def pair(self, document: object, expected: bool | None) -> None:
        self.check(document, expected)
        self.check(selected(), True)

    def metadata_pair(self, value: object, native: object) -> None:
        for kind, expected in (("ProductDetailTitle", True), ("Other", False)):
            with self.subTest(kind=kind):
                bad = selected(module_type=kind, metadata=value)
                self.assertIs(is_bounded_json_tree(bad), False)
                self.pair(bad, None)
                control = selected(module_type=kind, metadata=copy.deepcopy(native))
                self.assertIs(is_bounded_json_tree(control), True)
                self.check(control, expected)

    def test_s01_selection_and_s05_ownership(self) -> None:
        rows: tuple[tuple[str, dict[str, object], bool], ...] = (
            ("missing", {}, False),
            ("unknown", {"module_type": "Other", "version": None}, False),
            ("nonstring-before-bad-version", {"module_type": 7, "version": []}, False),
            ("nonzero-ignores-data", selected(version=1, module_data=None), False),
            ("unknown-generic", {"module_data": {"title": "raw"}}, False),
            (
                "unknown-type-generic",
                selected(module_type="Other", module_data={"title": "raw"}),
                False,
            ),
            ("selected-no-fallback", selected(module_data={"title": "raw"}), False),
            ("empty", selected(), True),
            (
                "standalone-invalid-record",
                selected(module_data={"data_by_tcin": [None]}),
                True,
            ),
        )
        for label, document, expected in rows:
            with self.subTest(case=label):
                before = copy.deepcopy(document)
                self.pair(document, expected)
                self.assertEqual(document, before)
        leaf: list[object] = [1]
        nested: dict[str, object] = {"items": leaf}
        record: dict[str, object] = {"tcin": TCIN, "title": "raw", "nested": nested}
        records: list[object] = [record, {"tcin": "bad", "title": None}, None]
        data: dict[str, object] = {"data_by_tcin": records}
        document = selected(module_data=data)
        before = copy.deepcopy(document)
        self.check(document, True)
        self.assertEqual(document, before)
        for actual, original in (
            (document["module_data"], data),
            (data["data_by_tcin"], records),
            (records[0], record),
            (record["nested"], nested),
            (nested["items"], leaf),
        ):
            self.assertIs(actual, original)

    def test_s02_native_field_matrix(self) -> None:
        values: tuple[tuple[str, Factory], ...] = (
            ("missing", lambda: None),
            ("null", lambda: None),
            ("bool", lambda: False),
            ("int", lambda: 0),
            ("float", lambda: 0.0),
            ("string", lambda: "unknown"),
            ("list", lambda: []),
            ("dict", lambda: {}),
        )
        fields: tuple[tuple[str, tuple[bool | None, ...]], ...] = (
            ("module_type", (False,) * 8),
            ("version", (False, None, None, True, None, None, None, None)),
            ("module_data", (False, None, None, None, None, None, None, False)),
            ("data_by_tcin", (False, None, None, None, None, None, True, None)),
        )
        for field, outcomes in fields:
            for (label, factory), expected in zip(values, outcomes, strict=True):
                with self.subTest(field=field, row=label):
                    document = selected()
                    parent = (
                        cast("dict[str, object]", document["module_data"])
                        if field == "data_by_tcin"
                        else document
                    )
                    if label == "missing":
                        del parent[field]
                    else:
                        parent[field] = factory()
                    self.pair(document, expected)
                    self.check(selected(unknown=factory()), True)

    def test_s03_invalid_identifiers(self) -> None:
        counts: CallbackCounts = dict.fromkeys(CALLBACK_NAMES, 0)
        rows: tuple[tuple[str, object], ...] = (
            ("empty", ""),
            ("short", "1234567"),
            ("long", "123456789"),
            ("ascii", "1234567a"),
            ("newline", "1234567\n"),
            ("unicode", "\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18"),
            ("null", None),
            ("bool", True),
            ("integer", 12345678),
            ("list", []),
            ("dict", {}),
            ("hostile-string", HostileString(TCIN, counts)),
            ("hostile-object", HostileObject(counts)),
        )
        for label, identifier in rows:
            with self.subTest(identifier=label):
                native, hostile = selected(), HostileDict(counts)
                before = copy.deepcopy(native)
                self.check(hostile, None, identifier, 0)
                self.check(native, None, identifier, 0)
                self.assertEqual(native, before)
                self.assertIs(hostile.counts, counts)
                if label.startswith("hostile-"):
                    self.assertIs(
                        cast("HostileObject | HostileString", identifier).counts, counts
                    )
                self.assertEqual(counts, dict.fromkeys(CALLBACK_NAMES, 0))
                self.check(selected(), True)

    def test_s04_hostile_roots_and_descendants(self) -> None:
        counts: CallbackCounts = dict.fromkeys(CALLBACK_NAMES, 0)
        factories: tuple[tuple[str, Callable[[CallbackCounts], object]], ...] = (
            ("object", HostileObject),
            ("dict", HostileDict),
            ("list", HostileList),
            ("string", lambda counters: HostileString(TCIN, counters)),
        )
        for label, factory in factories:
            with self.subTest(fixture=label):
                root, descendant = factory(counts), factory(counts)
                for fixture in (root, descendant):
                    self.assertIs(cast("HostileObject", fixture).counts, counts)
                self.assertIs(is_bounded_json_tree(root), False)
                self.pair(root, None)
                self.metadata_pair(descendant, {"items": [None, True, TCIN]})
                self.assertEqual(counts, dict.fromkeys(CALLBACK_NAMES, 0))

    def test_s04_native_malformed_and_boundaries(self) -> None:
        root_values: tuple[object, ...] = (None, True, 0, 1.0, "native", [])
        for label, root in zip(
            ["null", "bool", "int", "float", "string", "list"], root_values, strict=True
        ):
            with self.subTest(root=label):
                self.assertIs(is_bounded_json_tree(root), False)
                self.pair(root, None)
        cycle: list[object] = []
        cycle.append(cycle)
        shared: list[object] = []
        bad: tuple[tuple[str, object], ...] = (
            ("cycle", cycle),
            ("alias", [shared, shared]),
            ("nan", float("nan")),
            ("positive-infinity", float("inf")),
            ("negative-infinity", -float("inf")),
            ("positive-integer", 10**4096),
            ("negative-integer", -(10**4096)),
        )
        for label, value in bad:
            with self.subTest(metadata=label):
                self.metadata_pair(
                    value, cast("list[object]", [[], [], 1.0, 10**4096 - 1])
                )
        keys = ("module_type", "version", "module_data", "data_by_tcin", "metadata")
        overhead = sum(map(len, keys)) + len("ProductDetailTitle")
        self.assertEqual(overhead, 67)
        for label in ("text", "nodes", "depth"):
            for excess in (0, 1):
                with self.subTest(bound=label, excess=excess):
                    if label == "text":
                        value = "x" * (2_000_000 - overhead + excess)
                    elif label == "nodes":
                        value = [None] * (10_000 - 6 + excess)
                    else:
                        value = None
                        for _ in range(31 + excess):
                            value = [value]
                    document = selected(metadata=value)
                    self.assertIs(is_bounded_json_tree(document), excess == 0)
                    self.pair(document, None if excess else True)

    def test_s06_failure_restoration_recovery(self) -> None:
        for failure in (RuntimeError, KeyboardInterrupt, SystemExit):
            with self.subTest(failure=failure.__name__), prior_trace() as prior:
                events: list[str] = []
                result: bool | None = False
                caught: BaseException | None = None
                try:
                    try:
                        result = probe_calls(
                            lambda: selection.is_title_module(selected(), TCIN),
                            is_bounded_json_tree.__code__,
                            events,
                            failure,
                        )
                    except (KeyboardInterrupt, SystemExit) as error:
                        caught = error
                    finally:
                        restored = sys.gettrace()
                finally:
                    sys.settrace(prior)
                self.assertIs(restored, prior)
                self.assertEqual(events, ["call"])
                if failure is RuntimeError:
                    self.assertIsNone(result)
                    self.assertIsNone(caught)
                else:
                    self.assertIs(type(caught), failure)
                    self.assertEqual(cast("BaseException", caught).args, ())
                self.check(selected(), True)
                self.assertIs(sys.gettrace(), prior)

    def test_s07_real_binding_and_static_grammar(self) -> None:
        function = selection.is_title_module
        self.assertIs(function.__globals__, vars(selection))
        protected = {
            "is_target_tcin": is_target_tcin,
            "is_bounded_json_tree": is_bounded_json_tree,
        }
        for name, binding in protected.items():
            self.assertIs(function.__globals__[name], binding)
        tree = ast.parse(inspect.getsource(selection))
        definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.assertEqual(len(definitions), 1)
        definition = definitions[0]
        self.assertEqual(definition.name, "is_title_module")
        self.assertEqual(
            [arg.arg for arg in definition.args.args], ["module", "expected_tcin"]
        )
        statement = definition.body[1]
        if not isinstance(statement, ast.Try):
            raise AssertionError("missing admission try")
        prefix = ast.parse(
            "if not is_target_tcin(expected_tcin):\n    return None\n"
            "if not is_bounded_json_tree(module):\n    return None\n"
        ).body
        for actual, expected in zip(statement.body[:2], prefix, strict=True):
            self.assertEqual(ast.dump(actual), ast.dump(expected))
        import_spec = ast.parse(
            "from typing import cast\n"
            "from agent_household.json_tree import is_bounded_json_tree\n"
            "from agent_household.target_tcin import is_target_tcin\n"
        ).body
        actual_imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        self.assertEqual(
            list(map(ast.dump, actual_imports)), list(map(ast.dump, import_spec))
        )
        scopes = (ast.Global, ast.Nonlocal, ast.Delete, ast.Match)
        reserved = {*protected, "type", "cast"}
        definitions_forbidden = (ast.ClassDef, ast.AsyncFunctionDef, ast.Import)
        calls: list[str] = []
        for node in ast.walk(tree):
            self.assertNotIsInstance(node, scopes + definitions_forbidden)
            if isinstance(node, (ast.Attribute, ast.Subscript)):
                self.assertNotIsInstance(node.ctx, ast.Store)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                self.assertNotIn(node.id, reserved)
            if isinstance(node, ast.arg):
                self.assertNotIn(node.arg, reserved)
            if isinstance(node, ast.ExceptHandler):
                self.assertNotIn(node.name, reserved)
            if isinstance(node, ast.FunctionDef):
                self.assertIs(node, definition)
            if isinstance(node, ast.Call):
                self.assertIsInstance(node.func, (ast.Name, ast.Attribute))
                if isinstance(node.func, ast.Name):
                    self.assertIn(node.func.id, {*protected, "type", "cast"})
                    if node.func.id in protected:
                        calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    self.assertEqual(node.func.attr, "get")
                    self.assertIsInstance(node.func.value, ast.Name)
        self.assertEqual(calls, ["is_target_tcin", "is_bounded_json_tree"])
        for node in tree.body:
            self.assertIsInstance(node, (ast.Expr, ast.ImportFrom, ast.FunctionDef))
            if isinstance(node, ast.Expr):
                self.assertIsInstance(node.value, ast.Constant)
