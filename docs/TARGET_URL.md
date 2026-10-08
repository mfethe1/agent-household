# Target canonical product URL helper

`agent_household.target_url.validate_product_url(url, expected_tcin)` validates
exact built-in strings and returns the original URL object without normalization.
Invalid values raise `ValueError("invalid Target product URL")` without echoing inputs.

The only accepted URL form is `https://www.target.com/p/<slug>/-/A-<tcin>`.
TCIN is eight ASCII decimal digits matching the separately supplied identifier.
Slug has 1–160 lowercase ASCII alphanumeric characters and single internal
hyphens separating nonempty segments. Total URL length is at most 512 characters.
Queries (including preselect), fragments, credentials, explicit ports, encodings,
Unicode, whitespace and alternate hosts or paths are rejected.

This pure opt-in helper performs no IO and is not exported from package init.
Tests contain synthetic URL cases; they prove only deterministic validation.
It does not fetch or parse Target content, observe price/stock/labels, produce an
Offer, authorize ordering, or integrate private household data. The real byte
parser, production transport and live qualification remain separate pending work.
