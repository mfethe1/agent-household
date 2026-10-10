# Target canonical product URL helper

`agent_household.target_url.validate_product_url(url, expected_tcin)` validates
exact built-in strings and returns the original URL object without normalization.
Invalid values raise `ValueError("invalid Target product URL")` without echoing inputs.

The only accepted URL form is `https://www.target.com/p/<slug>/-/A-<tcin>`.
TCIN is eight ASCII decimal digits matching the separately supplied identifier.
Slug is 1–160 characters, hyphens included: lowercase ASCII alphanumeric
segments separated by single internal hyphens. Total URL length is at most
512 characters.
Queries (including preselect), fragments, credentials, explicit ports, encodings,
Unicode, whitespace and alternate hosts or paths are rejected.

This pure opt-in helper performs no IO and is not exported from package init.
Tests contain synthetic URL cases; they prove only deterministic validation.
It does not fetch or parse Target content, observe price/stock/labels, produce an
Offer, authorize ordering, or integrate private household data. The real byte
parser, production transport and live qualification remain separate pending work.

## Provenance

The canonical URL grammar above, including its exactly-eight-ASCII-digit TCIN,
has no recorded source or evidence level (GOAL_PROMPT.md: documented,
source-inspected, live-tested or unavailable) in this repository. Both are
unverified assumptions until the P0-01 capability matrix (`docs/specs/SPEC-01.md`)
records one; passing tests show only that this helper enforces them.
