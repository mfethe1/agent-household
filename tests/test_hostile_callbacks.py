"""Direct callback contracts and immediate shipped-consumer proofs."""

import io
import unittest
from collections.abc import Callable, Iterator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from typing import cast

from hostile_callbacks import (
    CALLBACK_NAMES,
    CallbackCounts,
    HostileDict,
    HostileList,
    HostileObject,
    HostileString,
)

from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_tcin import is_target_tcin

Fixture = HostileObject | HostileString | HostileDict | HostileList
Factory = Callable[[CallbackCounts], Fixture]
Operation = Callable[[Fixture], object]

_FIXTURES: tuple[tuple[str, Factory, type[Fixture], Callable[[], object]], ...] = (
    ("object", HostileObject, HostileObject, lambda: None),
    (
        "string",
        lambda counts: HostileString("01234567", counts),
        HostileString,
        lambda: "01234567",
    ),
    ("dict", HostileDict, HostileDict, lambda: {}),
    ("list", HostileList, HostileList, lambda: []),
)
_OPERATIONS: tuple[tuple[str, Operation, Callable[[], object]], ...] = (
    ("len", lambda value: len(value), lambda: len("native")),
    ("iter", lambda value: iter(value), lambda: iter("native")),
    ("str", lambda value: str(value), lambda: str(12)),
    ("repr", lambda value: repr(value), lambda: repr(12)),
    ("eq", lambda value: value == "native", lambda: "native" == "native"),
    ("bool", lambda value: bool(value), lambda: bool("native")),
    ("getitem", lambda value: value[0], lambda: "native"[0]),
    (
        "get",
        lambda value: cast("HostileDict", value).get("key"),
        lambda: {"key": "native"}.get("key"),
    ),
)
_APPLICABLE = {
    "object": ("len", "iter", "str", "repr", "eq", "bool", "getitem"),
    "string": ("len", "iter", "str", "repr", "eq", "bool", "getitem"),
    "dict": CALLBACK_NAMES,
    "list": ("len", "iter", "str", "repr", "eq", "bool", "getitem"),
}


def _counts() -> CallbackCounts:
    return dict.fromkeys(CALLBACK_NAMES, 0)


def _reset(counts: CallbackCounts) -> None:
    for name in CALLBACK_NAMES:
        counts[name] = 0


class HostileCallbackTests(unittest.TestCase):
    @contextmanager
    def _silent(self) -> Iterator[None]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            yield
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def _shape(self, fixture: Fixture, expected_type: type[Fixture]) -> None:
        self.assertIs(type(fixture), expected_type)
        if isinstance(fixture, HostileString):
            self.assertEqual(str.__str__(fixture), "01234567")
            self.assertEqual(str.__len__(fixture), 8)
        elif isinstance(fixture, HostileDict):
            self.assertEqual(dict[object, object].__len__(fixture), 0)
        elif isinstance(fixture, HostileList):
            self.assertEqual(list[object].__len__(fixture), 0)
        else:
            self.assertIs(type(fixture), HostileObject)

    def test_constructor_safety_and_isolation(self) -> None:
        self.assertEqual(
            CALLBACK_NAMES,
            ("len", "iter", "str", "repr", "eq", "bool", "getitem", "get"),
        )
        with self._silent():
            for label, factory, expected_type, _native in _FIXTURES:
                with self.subTest(fixture=label):
                    first_counts = _counts()
                    second_counts = _counts()
                    first = factory(first_counts)
                    second = factory(second_counts)
                    self.assertIs(first.counts, first_counts)
                    self.assertIs(second.counts, second_counts)
                    self.assertIsNot(first_counts, second_counts)
                    self._shape(first, expected_type)
                    self._shape(second, expected_type)
                    self.assertEqual(first_counts, _counts())
                    self.assertEqual(second_counts, _counts())
                    with self.assertRaises(RuntimeError) as raised:
                        len(first)
                    self.assertEqual(raised.exception.args, ("len",))
                    expected = _counts()
                    expected["len"] = 1
                    self.assertEqual(first_counts, expected)
                    self.assertEqual(second_counts, _counts())

    def test_operation_matrix(self) -> None:
        with self._silent():
            for label, factory, _expected_type, _native in _FIXTURES:
                counts = _counts()
                fixture = factory(counts)
                for name, operation, native_operation in _OPERATIONS:
                    if name not in _APPLICABLE[label]:
                        continue
                    with self.subTest(fixture=label, operation=name):
                        _reset(counts)
                        native_operation()
                        self.assertEqual(counts, _counts())
                        for repetition in (1, 2):
                            with self.assertRaises(RuntimeError) as raised:
                                operation(fixture)
                            self.assertEqual(raised.exception.args, (name,))
                            expected = _counts()
                            expected[name] = repetition
                            self.assertEqual(counts, expected)
                        self.assertIs(fixture.counts, counts)

    def test_target_tcin_consumer(self) -> None:
        invalid: tuple[object, ...] = (
            "",
            "1234567",
            "123456789",
            "\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18",
            "1234567a",
            12345678,
            None,
            {},
            [],
        )
        with self._silent():
            self.assertIs(is_target_tcin("01234567"), True)
            for index, value in enumerate(invalid):
                with self.subTest(control=index):
                    self.assertIs(is_target_tcin(value), False)
            for label, factory, expected_type, _native in _FIXTURES:
                with self.subTest(fixture=label):
                    counts = _counts()
                    fixture = factory(counts)
                    original = fixture
                    self.assertIs(is_target_tcin(fixture), False)
                    self.assertTrue(fixture is original)
                    self._shape(fixture, expected_type)
                    self.assertIs(fixture.counts, counts)
                    self.assertEqual(counts, _counts())

    def test_bounded_json_tree_consumer(self) -> None:
        with self._silent():
            selected = {"tcin": "01234567", "title": "raw"}
            self.assertIs(is_bounded_json_tree(selected), True)
            self.assertEqual(selected, {"tcin": "01234567", "title": "raw"})
            for label, factory, expected_type, native in _FIXTURES:
                with self.subTest(fixture=label):
                    root_counts = _counts()
                    root = factory(root_counts)
                    original_root = root
                    self.assertIs(is_bounded_json_tree(root), False)
                    self.assertTrue(root is original_root)
                    self._shape(root, expected_type)
                    self.assertIs(root.counts, root_counts)
                    self.assertEqual(root_counts, _counts())
                    nested_counts = _counts()
                    nested = factory(nested_counts)
                    record: dict[str, object] = {
                        "tcin": "01234567",
                        "title": "raw",
                        "metadata": nested,
                    }
                    self.assertIs(is_bounded_json_tree(record), False)
                    self.assertTrue(record["metadata"] is nested)
                    self.assertEqual(record["tcin"], "01234567")
                    self.assertEqual(record["title"], "raw")
                    self._shape(nested, expected_type)
                    self.assertIs(nested.counts, nested_counts)
                    self.assertIsNot(root_counts, nested_counts)
                    self.assertEqual(nested_counts, _counts())
                    self.assertEqual(root_counts, _counts())
                    counterpart = native()
                    control: dict[str, object] = {
                        "tcin": "01234567",
                        "title": "raw",
                        "metadata": counterpart,
                    }
                    self.assertIs(is_bounded_json_tree(control), True)
                    self.assertTrue(control["metadata"] is counterpart)
                    self.assertEqual(control["tcin"], "01234567")
                    self.assertEqual(control["title"], "raw")

    def test_silence_and_caller_ownership(self) -> None:
        with self._silent():
            for label, factory, _expected_type, _native in _FIXTURES:
                with self.subTest(fixture=label):
                    counts = _counts()
                    other_counts = _counts()
                    fixture = factory(counts)
                    other = factory(other_counts)
                    with self.assertRaises(RuntimeError) as raised:
                        repr(fixture)
                    self.assertEqual(raised.exception.args, ("repr",))
                    expected = _counts()
                    expected["repr"] = 1
                    self.assertEqual(counts, expected)
                    self.assertEqual(other_counts, _counts())
                    _reset(counts)
                    self.assertIs(is_target_tcin(fixture), False)
                    self.assertIs(is_bounded_json_tree(fixture), False)
                    self.assertIs(fixture.counts, counts)
                    self.assertIs(other.counts, other_counts)
                    counts["get"] = 7
                    self.assertEqual(fixture.counts["get"], 7)
                    self.assertEqual(other_counts, _counts())
                    _reset(counts)
                    self.assertEqual(counts, _counts())


if __name__ == "__main__":
    unittest.main()
