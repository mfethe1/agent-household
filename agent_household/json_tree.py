"""Pure, opt-in bounds for an already-materialized synthetic JSON tree."""

import math
from typing import cast

_NODE_LIMIT = 10_000
_DEPTH_LIMIT = 32
_TEXT_LIMIT = 2_000_000
_INTEGER_LIMIT = 10**4096


def is_bounded_json_tree(document: object) -> bool:
    """Validate native JSON values without mutation, callbacks or diagnostics.

    Cancellation is not swallowed. Concurrent mutation has no snapshot guarantee.
    Bounds apply after materialization, not to raw JSON decoding or allocation.
    """
    try:
        return _walk(document)
    except Exception:
        return False


def _walk(document: object) -> bool:
    if type(document) is not dict:
        return False
    pending: list[tuple[object, int]] = [(document, 0)]
    containers: set[int] = set()
    visited = 0
    text_left = _TEXT_LIMIT
    while pending:
        value, depth = pending.pop()
        visited += 1
        if visited > _NODE_LIMIT or depth > _DEPTH_LIMIT:
            return False
        kind = type(value)
        if kind is dict or kind is list:
            identity = id(value)
            if identity in containers:
                return False
            containers.add(identity)
            if kind is dict:
                mapping = cast("dict[object, object]", value)
                if len(mapping) > _NODE_LIMIT - visited - len(pending):
                    return False
                for key, child in mapping.items():
                    if type(key) is not str:
                        return False
                    size = len(key)
                    if size > text_left:
                        return False
                    text_left -= size
                    pending.append((child, depth + 1))
            else:
                sequence = cast("list[object]", value)
                if len(sequence) > _NODE_LIMIT - visited - len(pending):
                    return False
                pending.extend((child, depth + 1) for child in sequence)
        elif kind is str:
            size = len(cast("str", value))
            if size > text_left:
                return False
            text_left -= size
        elif kind is int:
            integer = cast("int", value)
            if not -_INTEGER_LIMIT < integer < _INTEGER_LIMIT:
                return False
        elif kind is float:
            if not math.isfinite(cast("float", value)):
                return False
        elif kind is not bool and value is not None:
            return False
    return True
