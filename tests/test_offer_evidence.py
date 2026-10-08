"""Synthetic closed-schema qualification; no retailer or household fixtures."""

import json
import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta, timezone
from decimal import localcontext
from typing import cast
from zoneinfo import ZoneInfo

from agent_household import Observation, Offer, Quote, normalize_offer, quote_line

NOW = datetime(2026, 1, 1, 12, tzinfo=UTC)


def fixture() -> dict[str, object]:
    return {
        "schema_version": 1, "retailer": "synthetic", "channel": "pickup",
        "product_id": "p", "seller_id": "s", "variant_id": "v", "store_id": "x",
        "fulfillment": "pickup", "stock": "available", "currency": "USD",
        "pack_quantity": "2", "pack_unit": "each", "price_cents": 199,
        "observation": {"source_kind": "synthetic_fixture",
                        "observed_at": "2026-01-01T12:00:00Z", "body_sha256": "a" * 64},
        "label_status": "unknown",
    }


def normalized(data: dict[str, object]) -> Offer:
    return normalize_offer(json.dumps(data), NOW)


class DatetimeSubclass(datetime):
    """Exercise exact datetime type validation."""


class SchemaTests(unittest.TestCase):
    def test_valid_and_key_order(self) -> None:
        data = fixture()
        reversed_data = dict(reversed(list(data.items())))
        self.assertEqual(normalized(data), normalized(reversed_data))
        with localcontext() as context:
            context.prec = 1
            self.assertEqual(normalized(data).pack_quantity, "2")
        for price in (None, 0, 1_000_000):
            data["price_cents"] = price
            self.assertEqual(normalized(data).price_cents, price)
        for key in ("retailer", "channel", "product_id", "seller_id", "variant_id",
                    "store_id", "fulfillment"):
            data[key] = None
            self.assertIsNotNone(normalized(data))

    def test_closed_keys_and_types(self) -> None:
        for key in fixture():
            data = fixture()
            del data[key]
            with self.subTest(missing=key), self.assertRaises(ValueError):
                normalized(data)
            wrong_values: tuple[object, ...] = ([], {}, True, 1.5)
            for wrong in wrong_values:
                data = fixture()
                data[key] = wrong
                with self.subTest(key=key, wrong=wrong), self.assertRaises(ValueError):
                    normalized(data)
        data = fixture()
        data["extra"] = 1
        with self.assertRaises(ValueError):
            normalized(data)
        for value in (0, 2, "1", None):
            data = fixture()
            data["schema_version"] = value
            with self.assertRaises(ValueError):
                normalized(data)

    def test_strings_and_enums(self) -> None:
        for key in fixture():
            if key in ("schema_version", "price_cents", "observation"):
                continue
            for value in ("", "a" * 257, "x\n", "\u007f", "\u0080", "\ud800"):
                data = fixture()
                data[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    normalized(data)
        for key in ("retailer", "product_id", "seller_id", "variant_id", "store_id"):
            data = fixture()
            data[key] = " \t "
            with self.assertRaises(ValueError):
                normalized(data)
        for key in ("channel", "fulfillment", "stock", "currency",
                    "pack_unit", "label_status"):
            data = fixture()
            data[key] = "complete"
            with self.assertRaises(ValueError):
                normalized(data)

    def test_quantities_and_prices(self) -> None:
        for value in ("0", "1000000.000001", "1e2", "+1", " 1", "\uff11", "1.",
                      "1.0000001", "1\n", "NaN", "9" * 33):
            data = fixture()
            data["pack_quantity"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalized(data)
        for value in ("0.000001", "1000000", "0002.00"):
            data = fixture()
            data["pack_quantity"] = value
            self.assertEqual(normalized(data).pack_quantity, value)
        for price in (-1, 1_000_001, True, 1.5, "199"):
            data = fixture()
            data["price_cents"] = price
            with self.assertRaises(ValueError):
                normalized(data)

    def test_observation(self) -> None:
        for key in ("source_kind", "observed_at", "body_sha256"):
            for value in (None, True, "x", "x\n"):
                data = fixture()
                observation = cast(dict[str, object], data["observation"])
                observation[key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    normalized(data)
            data = fixture()
            del cast(dict[str, object], data["observation"])[key]
            with self.assertRaises(ValueError):
                normalized(data)
        for date in ("2026-02-30T12:00:00Z", "2026-01-01T12:00:60Z",
                     "2026-01-01T12:00:00+00:00", "2026-01-01t12:00:00z",
                     "2026-01-01T12:00Z", "2026-01-01T12:00:00.0000001Z",
                     "2026-01-01T12:00:00.000001Z", "2026-01-01T12:00:00Z\n"):
            data = fixture()
            cast(dict[str, object], data["observation"])["observed_at"] = date
            with self.subTest(date=date), self.assertRaises(ValueError):
                normalized(data)
        for source in ("synthetic_fixture", "public_web"):
            data = fixture()
            cast(dict[str, object], data["observation"])["source_kind"] = source
            self.assertEqual(normalized(data).observation.source_kind, source)
        data = fixture()
        observation = cast(dict[str, object], data["observation"])
        observation["observed_at"] = "2025-01-01T12:00:00.000001Z"
        self.assertIsNotNone(normalized(data))
        cast(dict[str, object], data["observation"])["extra"] = "x"
        with self.assertRaises(ValueError):
            normalized(data)

    def test_json_boundaries(self) -> None:
        payload = json.dumps(fixture())
        duplicate = payload.replace(
            '"schema_version": 1', '"schema_version": 1, "schema_version": 1'
        )
        nested_duplicate = payload.replace(
            '"source_kind": "synthetic_fixture"',
            '"source_kind": "synthetic_fixture", "source_kind": "public_web"'
        )
        for bad in (duplicate, nested_duplicate,
                    '{"x":' * 5 + '0' + '}' * 5, "[]", "null", "1", '"text"',
                    payload.replace("199", "NaN"), payload.replace("199", "Infinity"),
                    payload + "!", "{", " " * 8193, "\ud800"):
            with self.subTest(bad=bad[:30]), self.assertRaises(ValueError):
                normalize_offer(bad, NOW)
        exact = payload + " " * (8192 - len(payload.encode()))
        self.assertEqual(normalize_offer(exact, NOW), normalize_offer(payload, NOW))
        with self.assertRaises(ValueError):
            normalize_offer(exact + " ", NOW)
        data = fixture()
        data["product_id"] = 'escaped \\"{[} ☃'
        self.assertEqual(normalized(data).product_id, data["product_id"])

    def test_runtime_types_and_immutability(self) -> None:
        bad_values: tuple[object, ...] = (None, b"{}", {}, 1)
        for bad in bad_values:
            with self.assertRaises(ValueError):
                normalize_offer(cast(str, bad), NOW)
        for now in (None, "x", NOW.replace(tzinfo=None),
                    NOW.replace(tzinfo=ZoneInfo("UTC")),
                    DatetimeSubclass(2026, 1, 1, 12, tzinfo=UTC),
                    NOW.replace(tzinfo=timezone(timedelta(hours=1)))):
            with self.assertRaises(ValueError):
                normalize_offer(json.dumps(fixture()), cast(datetime, now))
        offer = normalized(fixture())
        for obj, field in ((offer, "price_cents"),
                           (offer.observation, "source_kind")):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, "other")


class OfferChild(Offer):
    """Subclass must not bypass exact-type check."""


class ObservationChild(Observation):
    """Subclass must not bypass exact-type check."""


class QuoteTests(unittest.TestCase):
    def test_arithmetic(self) -> None:
        offer = normalized(fixture())
        q: Quote = quote_line("5", "each", offer, NOW)
        self.assertEqual((q.pack_count, q.merchandise_total_cents), (3, 597))
        self.assertEqual(q.reasons, ("label_unqualified",))
        self.assertEqual(q.evidence_status, "needs_review")
        self.assertIsNone(q.all_in_total_cents)
        self.assertIs(q.approval_allowed, False)
        self.assertIs(q.ordering_available, False)
        for need, count in (("4", 2), ("4.000001", 3), ("0.000001", 1)):
            self.assertEqual(quote_line(need, "each", offer, NOW).pack_count, count)
        with localcontext() as context:
            context.prec = 1
            self.assertEqual(quote_line("5", "each", offer, NOW), q)
        for unit in ("each", "g", "kg", "ml", "l"):
            same = replace(offer, pack_unit=unit)
            self.assertEqual(quote_line("5", unit, same, NOW), q)
            for other in ("each", "g", "kg", "ml", "l"):
                if unit != other:
                    with self.assertRaises(ValueError):
                        quote_line("5", other, same, NOW)
        for price in (0, 1_000_000):
            priced = replace(offer, price_cents=price, pack_quantity="1")
            self.assertEqual(quote_line("10000", "each", priced, NOW).
                             merchandise_total_cents, 10000 * price)
            with self.assertRaises(ValueError):
                quote_line("10000.000001", "each", priced, NOW)
        field = "pack_count"
        with self.assertRaises(FrozenInstanceError):
            setattr(q, field, 1)

    def test_reasons_and_time(self) -> None:
        offer = normalized(fixture())
        for field in ("retailer", "channel", "product_id", "seller_id", "variant_id",
                      "store_id", "fulfillment"):
            q = quote_line("5", "each", replace(offer, **{field: None}), NOW)
            self.assertEqual(q.reasons, ("label_unqualified", "missing_identity"))
            self.assertEqual(q.evidence_status, "blocked")
        for stock in ("available", "unavailable", "unknown"):
            q = quote_line("5", "each", replace(offer, stock=stock), NOW)
            expected = ("label_unqualified",) if stock == "available" else (
                "label_unqualified", "stock_" + stock,
            )
            self.assertEqual(q.reasons, expected)
        for label in ("unknown", "partial"):
            for source in ("public_web", "synthetic_fixture"):
                changed = replace(offer, label_status=label, observation=replace(
                    offer.observation, source_kind=source,
                ))
                self.assertFalse(quote_line("1", "each", changed, NOW).approval_allowed)
        self.assertEqual(quote_line("1", "each", offer, NOW + timedelta(minutes=15)).
                         evidence_status, "needs_review")
        self.assertIn("stale", quote_line("1", "each", offer, NOW + timedelta(
            minutes=15, microseconds=1,
        )).reasons)
        with self.assertRaises(ValueError):
            quote_line("1", "each", offer, NOW - timedelta(microseconds=1))
        blocked = replace(offer, price_cents=None, stock="unknown", retailer=None)
        q = quote_line("1", "each", blocked, NOW + timedelta(minutes=16))
        self.assertEqual(q.reasons, ("label_unqualified", "missing_identity",
                                    "missing_price", "stale", "stock_unknown"))
        self.assertIsNone(q.merchandise_total_cents)
        with self.assertRaises(ValueError):
            tiny = replace(blocked, pack_quantity="0.000001")
            quote_line("1000000", "each", tiny, NOW)

    def test_bad_inputs_and_bypass(self) -> None:
        offer = normalized(fixture())
        bad_quantities: tuple[object, ...] = (
            None, True, {}, b"1", 1, "0", "-1", "1e2", "1\n", "1000001",
        )
        for value in bad_quantities:
            with self.assertRaises(ValueError):
                quote_line(cast(str, value), "each", offer, NOW)
        bad_units: tuple[object, ...] = (None, True, {}, "bad", "each\n")
        for value in bad_units:
            with self.assertRaises(ValueError):
                quote_line("1", cast(str, value), offer, NOW)
        bad_offers: tuple[object, ...] = (None, {}, "bad")
        for value in bad_offers:
            with self.assertRaises(ValueError):
                quote_line("1", "each", cast(Offer, value), NOW)
        for now in (NOW.replace(tzinfo=None), NOW.replace(tzinfo=ZoneInfo("UTC")),
                    DatetimeSubclass(2026, 1, 1, 12, tzinfo=UTC), None):
            with self.assertRaises(ValueError):
                quote_line("1", "each", offer, cast(datetime, now))
        bad_fields: tuple[object, ...] = ([], True, "bad\n", None)
        for key in fixture():
            for value in bad_fields:
                if value is None and key in ("retailer", "channel", "product_id",
                                            "seller_id", "variant_id", "store_id",
                                            "fulfillment", "price_cents"):
                    continue
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    quote_line("1", "each", replace(offer, **{key: value}), NOW)
        for key in ("source_kind", "observed_at", "body_sha256"):
            with self.assertRaises(ValueError):
                quote_line("1", "each", replace(offer, observation=replace(
                    offer.observation, **{key: "bad"},
                )), NOW)
        child = OfferChild(**{key: getattr(offer, key) for key in fixture()})
        with self.assertRaises(ValueError):
            quote_line("1", "each", child, NOW)
        observation = ObservationChild("public_web", "2026-01-01T12:00:00Z", "a" * 64)
        with self.assertRaises(ValueError):
            quote_line("1", "each", replace(offer, observation=observation), NOW)
        tampered = replace(offer)
        object.__setattr__(tampered, "price_cents", -1)
        with self.assertRaises(ValueError):
            quote_line("1", "each", tampered, NOW)

        object.__delattr__(tampered, "stock")
        with self.assertRaises(ValueError):
            quote_line("1", "each", tampered, NOW)

    def test_quote_invariants(self) -> None:
        q = quote_line("5", "each", normalized(fixture()), NOW)
        cases: dict[str, tuple[object, ...]] = {
            "evidence_status": (None, True, "complete", "blocked"),
            "reasons": ([], ("label_unqualified", "label_unqualified"), (),
                        ("label_unqualified", "x"), ("stale", "label_unqualified"),
                        ("label_unqualified", 1),
                        ("label_unqualified", "missing_price")),
            "pack_count": (True, 0, 10001, 1.0, None),
            "merchandise_total_cents": (True, -1, 10**10 + 1, 1.0, None),
            "currency": (True, "EUR", None), "all_in_total_cents": (0, True),
            "approval_allowed": (True, 0, None), "ordering_available": (True, 0, None),
        }
        for field, values in cases.items():
            for value in values:
                with (self.subTest(field=field, value=value),
                      self.assertRaises(ValueError)):
                    replace(q, **{field: value})
        with self.assertRaises(ValueError):
            replace(q, evidence_status="blocked", reasons=("label_unqualified",),
                    merchandise_total_cents=None)
        self.assertEqual(replace(q, merchandise_total_cents=10**10).
                         merchandise_total_cents, 10**10)


if __name__ == "__main__":
    unittest.main()
