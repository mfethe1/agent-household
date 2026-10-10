# Offline offer evidence arithmetic

Development module only, standard-library Python >=3.11, no install/backend claim.
`normalize_offer(payload_json, now_utc)` validates closed bounded JSON to frozen
Offer/Observation metadata. Digest integrity does not establish authenticity.

`quote_line(need_quantity, need_unit, offer, now_utc)` revalidates every exact
Offer/Observation field, rejects subclasses and future observations, then computes
positive ceiling pack count with integer micro-units. Units must be exactly equal;
no conversion, override or ambient Decimal context. Golden synthetic example:
need5 each, pack2 each, price199 cents =>3 packs/597 merchandise cents.

Age15minutes is inclusive; later is blocked. Missing identity/price, unknown or
unavailable stock also block. Label-unqualified is mandatory, so no result is
complete, approved or ordering-ready. `source_kind` and `label_status` are validated
and carried as metadata but do not currently change quote arithmetic, reasons or
approval; approval is never granted by this module. All-in totals stay null;
merchandise excludes taxes/fees. Quote validates constructor invariants, but a
manually constructed Quote does not prove normalized source evidence.

Pack count bound10000 times price bound1000000 reaches merchandise ceiling10^10.
A quote_line total exceeding10^10 is mathematically unreachable without first
violating count or price bounds; tests check those reachable failures and constructor
10^10/+1. The pack-count bound still rejects already-blocked offers.

No private data, live retailer collection/integration, dietary clearance, purchases,
shared-expense settlement, persistence or approvals. Synthetic fixtures alone cannot
qualify any source. Private/live program acceptance remains separate and incomplete.
