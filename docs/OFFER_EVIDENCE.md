# Closed offer schema — first #19 slice

`normalize_offer(payload_json, now_utc)` returns a frozen Offer/Observation.
Input follows the closed schema in issue #19: bounded UTF-8 JSON, duplicate keys
rejected, no arrays, root depth 1/max 4, exact integer USD cents, decimal-text
quantity, strict UTC timestamps and observation metadata. Stale evidence parses;
future evidence fails. Digests are metadata, not source authenticity.

This first slice provides structural validation only. `quote_line` and `Quote`
are NOT implemented; missing identity, stock and price remain unqualified.
No complete labels, dietary clearance, recommendation, money movement, private
household data or live integration are claimed. Fixtures are synthetic.
