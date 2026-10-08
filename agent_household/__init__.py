"""Offline offer metadata; no live retailer integration or approval."""

from .offer_evidence import Observation, Offer, normalize_offer

__all__ = ["Observation", "Offer", "normalize_offer"]
