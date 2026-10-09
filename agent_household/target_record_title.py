"""Collect one untrusted raw title from a stable, caller-owned record."""

from typing import cast

from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_tcin import is_target_tcin


def collect_record_title(
    record: object, expected_tcin: object
) -> tuple[str, ...] | None:
    """Return raw title facts, empty nonmatches, or rejection; never normalize."""
    try:
        if not is_target_tcin(expected_tcin):
            return None
        if not is_bounded_json_tree(record):
            return None
        if type(record) is not dict:
            return None
        mapping = cast("dict[str, object]", record)
        if "tcin" not in mapping:
            return ()
        tcin = mapping["tcin"]
        if type(tcin) is not str:
            return None
        if tcin != expected_tcin:
            return ()
        if "title" not in mapping:
            return None
        title = mapping["title"]
        if type(title) is not str:
            return None
        return (title,)
    except Exception:
        return None
