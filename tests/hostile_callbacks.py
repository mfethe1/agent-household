"""Caller-owned, test-only fixtures whose observable callbacks raise."""

from typing import Never, Self

CallbackCounts = dict[str, int]
CALLBACK_NAMES = ("len", "iter", "str", "repr", "eq", "bool", "getitem", "get")


class _Callbacks:
    counts: CallbackCounts

    def _hit(self, name: str) -> Never:
        self.counts[name] += 1
        raise RuntimeError(name)

    def __len__(self) -> int:
        self._hit("len")

    def __iter__(self) -> Never:
        self._hit("iter")

    def __str__(self) -> str:
        self._hit("str")

    def __repr__(self) -> str:
        self._hit("repr")

    def __eq__(self, _other: object, /) -> bool:
        self._hit("eq")

    def __bool__(self) -> bool:
        self._hit("bool")

    def __getitem__(self, _key: object, /) -> Never:
        self._hit("getitem")


class HostileObject(_Callbacks):
    def __init__(self, counts: CallbackCounts) -> None:
        self.counts = counts


class HostileString(_Callbacks, str):
    def __new__(cls, value: str, counts: CallbackCounts) -> Self:
        del counts
        return str.__new__(cls, value)

    def __init__(self, value: str, counts: CallbackCounts) -> None:
        del value
        self.counts = counts


class HostileDict(_Callbacks, dict[object, object]):
    def __init__(self, counts: CallbackCounts) -> None:
        dict[object, object].__init__(self)
        self.counts = counts

    def get(self, _key: object, _default: object = None, /) -> Never:
        self._hit("get")


class HostileList(_Callbacks, list[object]):
    def __init__(self, counts: CallbackCounts) -> None:
        list[object].__init__(self)
        self.counts = counts
