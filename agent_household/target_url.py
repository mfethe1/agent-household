"""Pure canonical Target product URL validation; no retailer observation."""

import re

_PRODUCT = re.compile(
    r"https://www\.target\.com/p/([a-z0-9]+(?:-[a-z0-9]+)*)/-/A-([0-9]{8})"
)


def validate_product_url(url: str, expected_tcin: str) -> str:
    """Return the unchanged URL or raise a fixed, non-disclosing ValueError."""
    if type(url) is not str or type(expected_tcin) is not str:
        raise ValueError("invalid Target product URL")
    if len(url) > 512 or re.fullmatch(r"[0-9]{8}", expected_tcin) is None:
        raise ValueError("invalid Target product URL")
    match = _PRODUCT.fullmatch(url)
    if match is None or len(match[1]) > 160 or match[2] != expected_tcin:
        raise ValueError("invalid Target product URL")
    return url
