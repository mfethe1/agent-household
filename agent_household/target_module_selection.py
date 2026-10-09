"""Pure bounded native title-module selection; records remain downstream."""

from typing import cast

from agent_household.json_tree import is_bounded_json_tree
from agent_household.target_tcin import is_target_tcin


def is_title_module(module: object, expected_tcin: object) -> bool | None:
    """Return selected, ignored, or malformed without consuming records."""
    try:
        if not is_target_tcin(expected_tcin):
            return None
        if not is_bounded_json_tree(module):
            return None
        mapping = cast("dict[str, object]", module)
        kind = mapping.get("module_type")
        if type(kind) is not str or kind != "ProductDetailTitle":
            return False
        version = mapping.get("version")
        if type(version) is not int:
            return None if "version" in mapping else False
        if version != 0:
            return False
        data = mapping.get("module_data")
        if type(data) is not dict:
            return None if "module_data" in mapping else False
        container = cast("dict[str, object]", data)
        if "data_by_tcin" not in container:
            return False
        return True if type(container["data_by_tcin"]) is list else None
    except Exception:
        return None
