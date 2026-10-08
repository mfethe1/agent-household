import unittest
from collections.abc import Iterator
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from agent_household.target_tcin import is_target_tcin

_CALLBACKS: dict[str, int] = dict.fromkeys(
    ("len", "iter", "str", "repr", "eq", "bool"), 0
)


def _record(name: str) -> None:
    _CALLBACKS[name] += 1


class PlainString(str):
    pass


class HostileString(str):
    def __len__(self) -> int:
        _record("len")
        return 8

    def __iter__(self) -> Iterator[str]:
        _record("iter")
        return iter("12345678")

    def __str__(self) -> str:
        _record("str")
        return "12345678"

    def __repr__(self) -> str:
        _record("repr")
        return "hostile string"

    def __eq__(self, other: object) -> bool:
        _record("eq")
        return False

    def __bool__(self) -> bool:
        _record("bool")
        return True


class HostileObject:
    def __len__(self) -> int:
        _record("len")
        return 8

    def __iter__(self) -> Iterator[str]:
        _record("iter")
        return iter("12345678")

    def __str__(self) -> str:
        _record("str")
        return "12345678"

    def __repr__(self) -> str:
        _record("repr")
        return "hostile object"

    def __eq__(self, other: object) -> bool:
        _record("eq")
        return False

    def __bool__(self) -> bool:
        _record("bool")
        return True


class TargetTcinTests(unittest.TestCase):
    def test_valid_exact_strings_return_exact_true(self) -> None:
        cases = ("12345678", "00000000", "01234567", "99999999")
        for value in cases:
            with self.subTest(value=value):
                self.assertIs(is_target_tcin(value), True)

    def test_every_length_edge_and_huge_string(self) -> None:
        lengths = [*range(8), *range(9, 17), 100_000]
        for length in lengths:
            with self.subTest(length=length):
                self.assertIs(is_target_tcin("1" * length), False)

    def test_every_ascii_nondigit_at_every_position(self) -> None:
        for codepoint in range(128):
            if ord("0") <= codepoint <= ord("9"):
                continue
            for position in range(8):
                with self.subTest(codepoint=codepoint, position=position):
                    value = "1" * position + chr(codepoint) + "1" * (7 - position)
                    self.assertIs(is_target_tcin(value), False)

    def test_unicode_digits_confusables_and_surrogates(self) -> None:
        cases = (
            ("arabic", "\u0661" * 8),
            ("fullwidth", "\uff11" * 8),
            ("devanagari", "\u0967" * 8),
            ("superscript", "\u00b2" * 8),
            ("mixed_digits", "123\u0664\uff15\u096c\u00b28"),
            ("zero_width", "123\u200b5678"),
            ("nbsp", "123\u00a05678"),
            ("latin_letter", "123O5678"),
            ("cyrillic_letter", "123\u041e5678"),
            ("greek_letter", "123\u039f5678"),
            ("high_surrogate", "123\ud8005678"),
            ("low_surrogate", "123\udfff5678"),
            ("surrogate_pair", "12\ud800\udc005678"),
        )
        for name, value in cases:
            with self.subTest(case=name):
                self.assertIs(is_target_tcin(value), False)

    def test_nonstring_types_return_exact_false(self) -> None:
        fixtures: list[object] = [
            None,
            False,
            True,
            12345678,
            12345678.0,
            b"12345678",
            list("12345678"),
            {"value": "12345678"},
            tuple("12345678"),
            set("12345678"),
            object(),
        ]
        for index, value in enumerate(fixtures):
            with self.subTest(index=index):
                self.assertIs(is_target_tcin(value), False)

    def test_string_subclasses_rejected_even_with_valid_payload(self) -> None:
        fixtures: list[object] = [PlainString("12345678"), PlainString("00000000")]
        for index, value in enumerate(fixtures):
            with self.subTest(index=index):
                self.assertIs(is_target_tcin(value), False)

    def test_hostile_fixtures_have_no_callbacks(self) -> None:
        fixtures: list[object] = [HostileString("12345678"), HostileObject()]
        for index, value in enumerate(fixtures):
            for name in _CALLBACKS:
                _CALLBACKS[name] = 0
            with self.subTest(index=index):
                self.assertIs(is_target_tcin(value), False)
                for name, count in _CALLBACKS.items():
                    with self.subTest(callback=name):
                        self.assertEqual(count, 0)

    def test_valid_and_invalid_calls_are_silent(self) -> None:
        fixtures: list[object] = [
            "12345678",
            "00000000",
            "",
            "1234567\n",
            "\u0661" * 8,
            None,
            b"12345678",
            HostileString("12345678"),
            HostileObject(),
        ]
        expected = [True, True, False, False, False, False, False, False, False]
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            results = [is_target_tcin(value) for value in fixtures]
        for index, (result, accepted) in enumerate(zip(results, expected, strict=True)):
            with self.subTest(index=index):
                self.assertIs(result, accepted)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def test_native_mutable_rejects_keep_identity_and_content(self) -> None:
        fixtures: list[object] = [[1, 2], {"key": 3}, {4, 5}]
        originals = tuple(fixtures)
        snapshots: list[object] = [[1, 2], {"key": 3}, {4, 5}]
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            results = [is_target_tcin(value) for value in fixtures]
        for index, value in enumerate(fixtures):
            with self.subTest(index=index):
                self.assertIs(results[index], False)
                self.assertIs(value, originals[index])
                self.assertEqual(value, snapshots[index])
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
