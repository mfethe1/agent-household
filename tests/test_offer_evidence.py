"""Synthetic closed-schema qualification; no retailer or household fixtures."""

import json
import re
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
        "schema_version": 1,
        "retailer": "synthetic",
        "channel": "pickup",
        "product_id": "p",
        "seller_id": "s",
        "variant_id": "v",
        "store_id": "x",
        "fulfillment": "pickup",
        "stock": "available",
        "currency": "USD",
        "pack_quantity": "2",
        "pack_unit": "each",
        "price_cents": 199,
        "observation": {
            "source_kind": "synthetic_fixture",
            "observed_at": "2026-01-01T12:00:00Z",
            "body_sha256": "a" * 64,
        },
        "label_status": "unknown",
    }


def normalized(data: dict[str, object]) -> Offer:
    return normalize_offer(json.dumps(data), NOW)


def guard(message: str) -> str:
    """Match one guard's whole message so an overlapping guard cannot pass."""
    return f"^{re.escape(message)}$"


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
        for key in (
            "retailer",
            "channel",
            "product_id",
            "seller_id",
            "variant_id",
            "store_id",
            "fulfillment",
        ):
            data[key] = None
            self.assertIsNotNone(normalized(data))

    def test_closed_keys_and_types(self) -> None:
        for key in fixture():
            data = fixture()
            del data[key]
            with (
                self.subTest(missing=key),
                self.assertRaisesRegex(ValueError, guard("invalid offer fields")),
            ):
                normalized(data)
            data = fixture()
            data[key] = []
            with (
                self.subTest(key=key, wrong=[]),
                self.assertRaisesRegex(ValueError, guard("arrays forbidden")),
            ):
                normalized(data)
            wrong_values: tuple[object, ...] = ({}, True, 1.5)
            for wrong in wrong_values:
                data = fixture()
                data[key] = wrong
                with self.subTest(key=key, wrong=wrong), self.assertRaises(ValueError):
                    normalized(data)
        data = fixture()
        data["extra"] = 1
        with self.assertRaisesRegex(ValueError, guard("invalid offer fields")):
            normalized(data)
        for value in (0, 2, "1", None):
            data = fixture()
            data["schema_version"] = value
            with self.assertRaisesRegex(ValueError, guard("unsupported schema")):
                normalized(data)

    def test_strings_and_enums(self) -> None:
        for key in fixture():
            if key in ("schema_version", "price_cents", "observation"):
                continue
            data = fixture()
            data[key] = ""
            with self.subTest(key=key, value=""), self.assertRaises(ValueError):
                normalized(data)
            for value in (
                "a" * 257,
                "x\n",
                "x\u001f",
                "\u007f",
                "\u0080",
                "x\u009f",
                "\ud800",
                "x\udfff",
            ):
                data = fixture()
                data[key] = value
                with (
                    self.subTest(key=key, value=value),
                    self.assertRaisesRegex(ValueError, guard("invalid string")),
                ):
                    normalized(data)
        for value in ("a" * 256, "x ~", "x\u00a0", "x\ud7ff", "x\ue000"):
            data = fixture()
            data["product_id"] = value
            with self.subTest(value=value):
                self.assertEqual(normalized(data).product_id, value)
        for key in ("retailer", "product_id", "seller_id", "variant_id", "store_id"):
            for value, message in (
                (" \t ", "invalid string"),
                (" \u00a0\u3000 ", "empty identity"),
            ):
                data = fixture()
                data[key] = value
                with (
                    self.subTest(key=key, value=value),
                    self.assertRaisesRegex(ValueError, guard(message)),
                ):
                    normalized(data)
        for key in (
            "channel",
            "fulfillment",
            "stock",
            "currency",
            "pack_unit",
            "label_status",
        ):
            data = fixture()
            data[key] = "complete"
            message = "unsupported currency" if key == "currency" else "invalid enum"
            with self.assertRaisesRegex(ValueError, guard(message)):
                normalized(data)

    def test_quantities_and_prices(self) -> None:
        bad_quantities: tuple[tuple[str, str], ...] = (
            ("0", "quantity outside bounds"),
            ("1000000.000001", "quantity outside bounds"),
            ("1e2", "invalid quantity"),
            ("+1", "invalid quantity"),
            (" 1", "invalid quantity"),
            ("\uff11", "invalid quantity"),
            ("1.", "invalid quantity"),
            ("1.0000001", "invalid quantity"),
            ("1\n", "invalid string"),
            ("NaN", "invalid quantity"),
            ("9" * 33, "invalid quantity"),
            ("0" * 32 + "1", "invalid quantity"),
        )
        for value, message in bad_quantities:
            data = fixture()
            data["pack_quantity"] = value
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, guard(message)),
            ):
                normalized(data)
        for value in ("0.000001", "1000000", "0002.00", "0" * 31 + "1"):
            data = fixture()
            data["pack_quantity"] = value
            self.assertEqual(normalized(data).pack_quantity, value)
        for price in (-1, 1_000_001, True, 1.5, "199"):
            data = fixture()
            data["price_cents"] = price
            with self.assertRaisesRegex(ValueError, guard("invalid price")):
                normalized(data)

    def test_observation(self) -> None:
        for key in ("source_kind", "observed_at", "body_sha256"):
            invalid = "invalid enum" if key == "source_kind" else "invalid observation"
            cases: tuple[tuple[object, str], ...] = (
                (None, "string required"),
                (True, "string required"),
                ("x", invalid),
                ("x\n", "invalid string"),
            )
            for value, message in cases:
                data = fixture()
                observation = cast(dict[str, object], data["observation"])
                observation[key] = value
                with (
                    self.subTest(key=key, value=value),
                    self.assertRaisesRegex(ValueError, guard(message)),
                ):
                    normalized(data)
            data = fixture()
            del cast(dict[str, object], data["observation"])[key]
            with self.assertRaisesRegex(
                ValueError, guard("invalid observation fields")
            ):
                normalized(data)
        for date in ("2026-02-30T12:00:00Z", "2026-01-01T12:00:60Z"):
            data = fixture()
            cast(dict[str, object], data["observation"])["observed_at"] = date
            with self.subTest(date=date), self.assertRaises(ValueError):
                normalized(data)
        bad_dates: tuple[tuple[str, str], ...] = (
            ("2026-01-01T12:00:00+00:00", "invalid observation"),
            ("2026-01-01t12:00:00z", "invalid observation"),
            ("2026-01-01T12:00Z", "invalid observation"),
            ("2026-01-01T12:00:00.0000001Z", "invalid observation"),
            ("2026-01-01T12:00:00.000001Z", "future observation"),
            ("2026-01-01T12:00:00Z\n", "invalid string"),
        )
        for date, message in bad_dates:
            data = fixture()
            cast(dict[str, object], data["observation"])["observed_at"] = date
            with (
                self.subTest(date=date),
                self.assertRaisesRegex(ValueError, guard(message)),
            ):
                normalized(data)
        for digits in range(1, 6):
            date = "2026-01-01T11:59:59." + "1" * digits + "Z"
            data = fixture()
            cast(dict[str, object], data["observation"])["observed_at"] = date
            with self.subTest(date=date):
                self.assertEqual(normalized(data).observation.observed_at, date)
        for digest in ("A" * 64, "a" * 63, "a" * 65, "g" * 64):
            data = fixture()
            cast(dict[str, object], data["observation"])["body_sha256"] = digest
            with (
                self.subTest(digest=digest),
                self.assertRaisesRegex(ValueError, guard("invalid observation")),
            ):
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
        with self.assertRaisesRegex(ValueError, guard("invalid observation fields")):
            normalized(data)

    def test_json_boundaries(self) -> None:
        payload = json.dumps(fixture())
        duplicate = payload.replace(
            '"schema_version": 1', '"schema_version": 1, "schema_version": 1'
        )
        nested_duplicate = payload.replace(
            '"source_kind": "synthetic_fixture"',
            '"source_kind": "synthetic_fixture", "source_kind": "public_web"',
        )
        guarded: tuple[tuple[str, str], ...] = (
            (duplicate, "duplicate key"),
            (nested_duplicate, "duplicate key"),
            ('{"x":' * 5 + "0" + "}" * 5, "JSON too deep"),
            ('{"x":' * 4 + "0" + "}" * 4, "invalid offer fields"),
            ("[]", "arrays forbidden"),
            ("null", "object required"),
            ("1", "object required"),
            ('"text"', "object required"),
            (payload.replace("199", "NaN"), "nonstandard JSON constant"),
            (payload.replace("199", "Infinity"), "nonstandard JSON constant"),
            (" " * 8193, "JSON too large"),
            ("\ud800", "invalid encoding"),
        )
        for bad, message in guarded:
            with (
                self.subTest(bad=bad[:30]),
                self.assertRaisesRegex(ValueError, guard(message)),
            ):
                normalize_offer(bad, NOW)
        for bad in (payload + "!", "{"):
            with self.subTest(bad=bad[:30]), self.assertRaises(ValueError):
                normalize_offer(bad, NOW)
        exact = payload + " " * (8192 - len(payload.encode()))
        self.assertEqual(normalize_offer(exact, NOW), normalize_offer(payload, NOW))
        with self.assertRaisesRegex(ValueError, guard("JSON too large")):
            normalize_offer(exact + " ", NOW)
        wide = fixture()
        wide["product_id"] = "\u2603" * 256
        text = json.dumps(wide, ensure_ascii=False)
        self.assertEqual(normalize_offer(text, NOW).product_id, wide["product_id"])
        multibyte = text + " " * (8192 - len(text))
        self.assertEqual(len(multibyte), 8192)
        self.assertGreater(len(multibyte.encode()), 8192)
        with self.assertRaisesRegex(ValueError, guard("JSON too large")):
            normalize_offer(multibyte, NOW)
        data = fixture()
        data["product_id"] = 'escaped \\"{[} ☃'
        self.assertEqual(normalized(data).product_id, data["product_id"])

    def test_runtime_types_and_immutability(self) -> None:
        bad_values: tuple[object, ...] = (None, b"{}", {}, 1)
        for bad in bad_values:
            with self.assertRaisesRegex(ValueError, guard("JSON string required")):
                normalize_offer(cast(str, bad), NOW)
        for now in (
            None,
            "x",
            NOW.replace(tzinfo=None),
            NOW.replace(tzinfo=ZoneInfo("UTC")),
            DatetimeSubclass(2026, 1, 1, 12, tzinfo=UTC),
            NOW.replace(tzinfo=timezone(timedelta(hours=1))),
        ):
            with self.assertRaisesRegex(
                ValueError, guard("exact UTC datetime required")
            ):
                normalize_offer(json.dumps(fixture()), cast(datetime, now))
        offer = normalized(fixture())
        for obj, field in ((offer, "price_cents"), (offer.observation, "source_kind")):
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
                    with self.assertRaisesRegex(
                        ValueError, guard("unit conversion is not supported")
                    ):
                        quote_line("5", other, same, NOW)
        for price in (0, 1_000_000):
            priced = replace(offer, price_cents=price, pack_quantity="1")
            self.assertEqual(
                quote_line("10000", "each", priced, NOW).merchandise_total_cents,
                10000 * price,
            )
            with self.assertRaisesRegex(ValueError, guard("pack count exceeds bound")):
                quote_line("10000.000001", "each", priced, NOW)
        field = "pack_count"
        with self.assertRaises(FrozenInstanceError):
            setattr(q, field, 1)

    def test_reasons_and_time(self) -> None:
        offer = normalized(fixture())
        for field in (
            "retailer",
            "channel",
            "product_id",
            "seller_id",
            "variant_id",
            "store_id",
            "fulfillment",
        ):
            q = quote_line("5", "each", replace(offer, **{field: None}), NOW)
            self.assertEqual(q.reasons, ("label_unqualified", "missing_identity"))
            self.assertEqual(q.evidence_status, "blocked")
        for stock in ("available", "unavailable", "unknown"):
            q = quote_line("5", "each", replace(offer, stock=stock), NOW)
            expected = (
                ("label_unqualified",)
                if stock == "available"
                else (
                    "label_unqualified",
                    "stock_" + stock,
                )
            )
            self.assertEqual(q.reasons, expected)
        # source_kind and label_status are inert metadata today: every
        # combination yields the identical Quote, ready or blocked. A change
        # that makes either field matter must update these baselines.
        blocked = replace(offer, price_cents=None, stock="unknown", retailer=None)
        unavailable = replace(offer, stock="unavailable")
        late = NOW + timedelta(minutes=16)
        ready_baseline = Quote(
            "needs_review", ("label_unqualified",), 3, 597, "USD", None, False, False
        )
        blocked_baseline = Quote(
            "blocked",
            (
                "label_unqualified",
                "missing_identity",
                "missing_price",
                "stale",
                "stock_unknown",
            ),
            3,
            None,
            "USD",
            None,
            False,
            False,
        )
        unavailable_baseline = Quote(
            "blocked",
            ("label_unqualified", "stock_unavailable"),
            3,
            597,
            "USD",
            None,
            False,
            False,
        )
        for label in ("unknown", "partial"):
            for source in ("public_web", "synthetic_fixture"):
                observation = replace(offer.observation, source_kind=source)
                ready = replace(offer, label_status=label, observation=observation)
                stuck = replace(blocked, label_status=label, observation=observation)
                gone = replace(unavailable, label_status=label, observation=observation)
                with self.subTest(label=label, source=source):
                    self.assertEqual(
                        quote_line("5", "each", ready, NOW), ready_baseline
                    )
                    self.assertEqual(
                        quote_line("5", "each", stuck, late), blocked_baseline
                    )
                    self.assertEqual(
                        quote_line("5", "each", gone, NOW), unavailable_baseline
                    )
        self.assertEqual(
            quote_line("1", "each", offer, NOW + timedelta(minutes=15)).evidence_status,
            "needs_review",
        )
        self.assertIn(
            "stale",
            quote_line(
                "1",
                "each",
                offer,
                NOW
                + timedelta(
                    minutes=15,
                    microseconds=1,
                ),
            ).reasons,
        )
        with self.assertRaisesRegex(ValueError, guard("future observation")):
            quote_line("1", "each", offer, NOW - timedelta(microseconds=1))
        q = quote_line("1", "each", blocked, late)
        self.assertEqual(
            q.reasons,
            (
                "label_unqualified",
                "missing_identity",
                "missing_price",
                "stale",
                "stock_unknown",
            ),
        )
        self.assertIsNone(q.merchandise_total_cents)
        with self.assertRaisesRegex(ValueError, guard("pack count exceeds bound")):
            tiny = replace(blocked, pack_quantity="0.000001")
            quote_line("1000000", "each", tiny, NOW)

    def test_bad_inputs_and_bypass(self) -> None:
        offer = normalized(fixture())
        bad_quantities: tuple[object, ...] = (
            None,
            True,
            {},
            b"1",
            1,
            "0",
            "-1",
            "1e2",
            "1\n",
            "1000001",
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
            with self.assertRaisesRegex(ValueError, guard("exact Offer required")):
                quote_line("1", "each", cast(Offer, value), NOW)
        for now in (
            NOW.replace(tzinfo=None),
            NOW.replace(tzinfo=ZoneInfo("UTC")),
            DatetimeSubclass(2026, 1, 1, 12, tzinfo=UTC),
            None,
        ):
            with self.assertRaisesRegex(
                ValueError, guard("exact UTC datetime required")
            ):
                quote_line("1", "each", offer, cast(datetime, now))
        bad_fields: tuple[object, ...] = ([], True, "bad\n", None)
        for key in fixture():
            for value in bad_fields:
                if value is None and key in (
                    "retailer",
                    "channel",
                    "product_id",
                    "seller_id",
                    "variant_id",
                    "store_id",
                    "fulfillment",
                    "price_cents",
                ):
                    continue
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    quote_line("1", "each", replace(offer, **{key: value}), NOW)
        for key in ("source_kind", "observed_at", "body_sha256"):
            invalid = "invalid enum" if key == "source_kind" else "invalid observation"
            with self.assertRaisesRegex(ValueError, guard(invalid)):
                quote_line(
                    "1",
                    "each",
                    replace(
                        offer,
                        observation=replace(
                            offer.observation,
                            **{key: "bad"},
                        ),
                    ),
                    NOW,
                )
        child = OfferChild(**{key: getattr(offer, key) for key in fixture()})
        with self.assertRaisesRegex(ValueError, guard("exact Offer required")):
            quote_line("1", "each", child, NOW)
        observation = ObservationChild("public_web", "2026-01-01T12:00:00Z", "a" * 64)
        with self.assertRaisesRegex(ValueError, guard("exact Observation required")):
            quote_line("1", "each", replace(offer, observation=observation), NOW)
        tampered = replace(offer)
        object.__setattr__(tampered, "price_cents", -1)
        with self.assertRaisesRegex(ValueError, guard("invalid price")):
            quote_line("1", "each", tampered, NOW)

        object.__delattr__(tampered, "stock")
        with self.assertRaisesRegex(ValueError, guard("missing dataclass field")):
            quote_line("1", "each", tampered, NOW)

    def test_quote_invariants(self) -> None:
        q = quote_line("5", "each", normalized(fixture()), NOW)
        shape = "reasons must be sorted, unique and unqualified"
        status = "invalid quote status or currency"
        total = "invalid merchandise total"
        permit = "quote cannot permit ordering or all-in pricing"
        cases: dict[str, tuple[tuple[object, str], ...]] = {
            "evidence_status": (
                (None, "string required"),
                (True, "string required"),
                ("complete", status),
                ("blocked", status),
            ),
            "reasons": (
                ([], "invalid reasons"),
                (("label_unqualified", "label_unqualified"), shape),
                ((), shape),
                (("label_unqualified", "x"), "invalid reasons"),
                (("stale", "label_unqualified"), shape),
                (("stale",), shape),
                (("missing_identity", "stale"), shape),
                (("label_unqualified", 1), "invalid reasons"),
                (("label_unqualified", "missing_price"), status),
            ),
            "pack_count": (
                (True, "invalid pack count"),
                (0, "invalid pack count"),
                (10001, "invalid pack count"),
                (1.0, "invalid pack count"),
                (None, "invalid pack count"),
            ),
            "merchandise_total_cents": (
                (True, total),
                (-1, total),
                (10**10 + 1, total),
                (1.0, total),
                (None, "price/reason mismatch"),
            ),
            "currency": (
                (True, "string required"),
                ("EUR", status),
                (None, "string required"),
            ),
            "all_in_total_cents": ((0, permit), (True, permit)),
            "approval_allowed": ((True, permit), (0, permit), (None, permit)),
            "ordering_available": ((True, permit), (0, permit), (None, permit)),
        }
        for field, values in cases.items():
            for value, message in values:
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaisesRegex(ValueError, guard(message)),
                ):
                    replace(q, **{field: value})
        with self.assertRaisesRegex(ValueError, guard(status)):
            replace(
                q,
                evidence_status="blocked",
                reasons=("label_unqualified",),
                merchandise_total_cents=None,
            )
        self.assertEqual(
            replace(q, merchandise_total_cents=10**10).merchandise_total_cents, 10**10
        )


if __name__ == "__main__":
    unittest.main()
