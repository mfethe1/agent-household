"""Bounded offline offer normalization; not evidence authenticity or approval."""

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, cast

_FIELDS: Final = {
    "schema_version", "retailer", "channel", "product_id", "seller_id",
    "variant_id", "store_id", "fulfillment", "stock", "currency",
    "pack_quantity", "pack_unit", "price_cents", "observation", "label_status",
}
_OBSERVATION: Final = {"source_kind", "observed_at", "body_sha256"}
_ENUMS: Final = {
    "channel": {"warehouse", "same_day", "shipped", "retail", "fresh", "pickup"},
    "fulfillment": {"pickup", "delivery", "shipping"},
    "stock": {"available", "unavailable", "unknown"},
    "pack_unit": {"each", "g", "kg", "ml", "l"},
    "label_status": {"unknown", "partial"},
    "source_kind": {"public_web", "synthetic_fixture"},
}
_QUANTITY: Final = re.compile(r"[0-9]+(?:\.[0-9]{1,6})?")
_DATE: Final = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z"
)
_DIGEST: Final = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class Observation:
    """Immutable metadata; digest integrity does not imply authenticity."""

    source_kind: str
    observed_at: str
    body_sha256: str


@dataclass(frozen=True)
class Offer:
    """Unqualified immutable offer; direct construction is not validation."""

    schema_version: int
    retailer: str | None
    channel: str | None
    product_id: str | None
    seller_id: str | None
    variant_id: str | None
    store_id: str | None
    fulfillment: str | None
    stock: str
    currency: str
    pack_quantity: str
    pack_unit: str
    price_cents: int | None
    observation: Observation
    label_status: str


def _text(value: object) -> str:
    if type(value) is not str:
        raise ValueError("string required")
    if len(value) > 256 or any(
        ord(c) < 32 or 127 <= ord(c) <= 159 or 55296 <= ord(c) <= 57343
        for c in value
    ):
        raise ValueError("invalid string")
    return value


def _enum(key: str, value: object) -> str:
    text = _text(value)
    if text not in _ENUMS[key]:
        raise ValueError("invalid enum")
    return text


def _identity(value: object) -> str | None:
    if value is None:
        return None
    text = _text(value)
    if not text.strip():
        raise ValueError("empty identity")
    return text


def _quantity(value: object) -> str:
    text = _text(value)
    if len(text) > 32 or _QUANTITY.fullmatch(text) is None:
        raise ValueError("invalid quantity")
    whole, _, fraction = text.partition(".")
    scaled = int(whole) * 1_000_000 + int(fraction.ljust(6, "0"))
    if not 0 < scaled <= 1_000_000_000_000:
        raise ValueError("quantity outside bounds")
    return text


def _pairs(items: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in items:
        _text(key)
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _constant(_value: str) -> object:
    raise ValueError("nonstandard JSON constant")


def _decode(payload: str) -> dict[str, object]:
    if type(payload) is not str:
        raise ValueError("JSON string required")
    try:
        if len(payload.encode("utf-8")) > 8192:
            raise ValueError("JSON too large")
    except UnicodeError as exc:
        raise ValueError("invalid encoding") from exc
    depth = 0
    quoted = False
    escaped = False
    for char in payload:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "[":
            raise ValueError("arrays forbidden")
        elif char == "{":
            depth += 1
            if depth > 4:
                raise ValueError("JSON too deep")
        elif char == "}":
            depth -= 1
    try:
        value: object = json.loads(
            payload, object_pairs_hook=_pairs, parse_constant=_constant
        )
    except (RecursionError, TypeError, OverflowError) as exc:
        raise ValueError("invalid JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("object required")
    data = cast(dict[str, object], value)
    if set(data) != _FIELDS:
        raise ValueError("invalid offer fields")
    return data


def normalize_offer(payload_json: str, now_utc: datetime) -> Offer:
    """Validate closed JSON; allow stale observations, reject future ones."""
    if type(now_utc) is not datetime or now_utc.tzinfo is not UTC:
        raise ValueError("exact UTC datetime required")
    data = _decode(payload_json)
    version = data["schema_version"]
    price = data["price_cents"]
    if type(version) is not int or version != 1:
        raise ValueError("unsupported schema")
    if price is not None and (type(price) is not int or not 0 <= price <= 1_000_000):
        raise ValueError("invalid price")
    if _text(data["currency"]) != "USD":
        raise ValueError("unsupported currency")
    observation = data["observation"]
    if not isinstance(observation, dict):
        raise ValueError("observation object required")
    observation = cast(dict[str, object], observation)
    if set(observation) != _OBSERVATION:
        raise ValueError("invalid observation fields")
    observed = _text(observation["observed_at"])
    digest = _text(observation["body_sha256"])
    if _DATE.fullmatch(observed) is None or _DIGEST.fullmatch(digest) is None:
        raise ValueError("invalid observation")
    instant = datetime.fromisoformat(observed[:-1] + "+00:00")
    if instant > now_utc:
        raise ValueError("future observation")
    return Offer(
        version, _identity(data["retailer"]),
        None if data["channel"] is None else _enum("channel", data["channel"]),
        _identity(data["product_id"]), _identity(data["seller_id"]),
        _identity(data["variant_id"]), _identity(data["store_id"]),
        (None if data["fulfillment"] is None
         else _enum("fulfillment", data["fulfillment"])),
        _enum("stock", data["stock"]), "USD", _quantity(data["pack_quantity"]),
        _enum("pack_unit", data["pack_unit"]), price,
        Observation(_enum("source_kind", observation["source_kind"]), observed, digest),
        _enum("label_status", data["label_status"]),
    )
