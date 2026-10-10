# Acceptance and evidence matrix

Every item below (A01–A25) is PENDING; see "Status and evidence recording". A written requirement is not a passing test.

## Retailers and shopping
- A01: Costco/Amazon/Target per-retailer, per-channel capability matrix; channels qualified separately (warehouse/shipped/same-day; Amazon retail/Fresh); unsupported operations explicit.
  - Operations: discovery, product details, local price/availability, authenticated cart read/add/change/remove, checkout handoff, order status, itemized receipts and refunds.
  - Each cell records access requirements, source, verification time, supported geography, limits, license/terms constraints and evidence level: documented, source-inspected, live-tested or unavailable.
- A02: Exact product/seller/pack/quantity/local fulfillment and fresh dietary-label evidence; unsafe/unknown match blocked. Drafts built from receipt history or calendar context never set attendance or hard dietary restrictions; both stay unknown until the user states them.
- A03: All-in basket comparison exposes unknown costs and usable-unit/waste assumptions.
- A04: Pre-existing cart lines preserved; concurrent user edit invalidates stale proposal; simultaneous restock drafts do not cause duplicate purchases.
- A05: Expired approval, changed price/slot/seller/quantity and unwanted subscription mode block submission. Approval binds an explicit substitution policy; no sensitive line, including any line under a hard dietary restriction, is auto-substituted; saved brands, split templates and fulfillment preferences never satisfy the approval gate.
- A06: Real phone handoff per required retailer preserves reviewed basket; user completes checkout only under separate exact approval.
- A07: Lost confirmation/crash produces UNKNOWN; authoritative order reconciliation prevents duplicate submission.
- A08: Split shipment, weighted item, substitution, partial cancellation and later return reconcile order/receipt/charge separately.

## Receipt capture and shared expenses
- A09: Phone image/digital multi-page receipt retained with original provenance, selected owner/uploader and separately recorded payers; extraction corrections are versioned and never alter the retained original evidence.
- A10: Low-confidence OCR and mismatched totals require correction; pre-tip bill is not presented as final restaurant spend.
- A11: Reimport plus photo upload plus revised receipt do not double-count; two legitimate identical purchases remain distinct.
- A12: Supported account source genuinely imports receipts; transaction-only source labeled incomplete; expired token/sync gap visible and upload fallback works.
- A13: Equal/percentage/fixed/item splits reconcile exactly, including deterministic rounding, shared dishes, split checks, taxes/tips/fees/discounts, multiple payers, cash and gift cards. Service charge and tip are distinct fields, never double-counted. Amounts are integer minor units; floating-point amounts rejected.
- A14: Unknown payer or unpaid remainder remains explicit; no fabricated paid amount.
- A15: Proposal, acceptance, dispute, member departure and guest identity claim tested; nonconsenting party is not silently assigned accepted debt.
- A16: Settled expense edit creates adjustment; partial refund, settlement reversal and participant-confirmed settlement preserve audit history. A recorded settlement is shown as user-reported, never as an executed or verified transfer; a receipt alone never marks an obligation settled.
- A17: Retailer gross spending, budget-category spending, personal allocated cost, outstanding reimbursement and received reimbursement are five separate projections; restaurant expenses categorized separately by default; every displayed balance, including who owes whom, explainable from source records; cross-currency netting rejected without explicit conversion.

## Security, recovery and experience
- A18: Negative user/group/guest authorization tests cover records, attachments, exports and agent tools, including shared retailer accounts.
- A19: Malicious receipt/product text cannot authorize actions; unsafe file/oversize upload rejected; model processing disclosure shown.
- A20: Backup restored into isolated environment rebuilds identical ledger projections and attachments; no secrets in logs/public artifacts.
- A21: Unlink/revocation, export, retention/deletion and backup expiry verified against published policy.
- A22: Phone/keyboard/screen-reader flows for upload, corrections, item allocation, approval and disputes; interrupted draft recovers. Accessibility conformance target not yet chosen; to be selected under P0-03 (GOAL_PROMPT names none).
- A23: Fresh self-hosted installation follows documented steps; missing integrations fail explicitly, not via seeded fake availability/debts.
- A24: Agent and UI mutation safety. The same mutation through an agent/MCP tool and through the UI takes one backend and one actor-bound authorization path and yields one ledger state; chat keeps no second ledger.
  - Previewing or dry-running a tool call executes nothing: no ledger, record or external effect.
  - Replaying an idempotency key has one effect; reusing a key with a different payload is rejected.
  - Each mutation yields a correlated action receipt.
  - A stale expected revision is rejected for every mutating record type, not only carts (A04).
- A25: Connector resilience. Network retries bounded and connector rate limits enforced; unavailable or stale connector state shown with manual recovery; a crash between external action and local confirmation is reconciled against the authoritative external record before any retry and never blindly repeats the action (purchases: A07).

A24 and A25 were appended without renumbering; ranges such as "A01–A23" elsewhere predate them.

## Pilot protocol (provisional thresholds; freeze before pilot)
Compare the same operator's manual workflow with system-assisted workflow on consented tasks of comparable complexity. Record task mix, sample size, failures and uncertainty; no general claim from a single demo.
- Aim for at least 25% lower median active user time for receipt-to-reviewed-split and basket preparation, measured separately; report review/correction time, not just agent runtime.
- Zero unapproved purchases, duplicate orders, unauthorized disclosures or silently incorrect accepted balances is a mandatory safety gate, not proof of future zero risk.
- Every accepted expense reconciles exactly; uncertain imports remain drafts. Report extraction field accuracy and correction rate separately from accounting reconciliation.
- Report handoff success/failure per retailer/channel, missed/duplicate imports, match corrections, disputes, model/connector costs and maintenance burden.
- Threshold changes after pilot begins require a recorded new protocol; do not tune the success definition after seeing results.

## Evidence rules
Synthetic adversarial fixtures demonstrate logic only. Actual supported integrations require separately authorized live evidence. Public summaries redact user data, tokens and account/order identifiers. Each acceptance item records exact commit, test command/result, evidence location and reviewer. No item marked passed from an implementer's assertion alone.

## Status and evidence recording
Every item is currently PENDING. Acceptance status per A-ID:
- PENDING: no evidence recorded.
- SYNTHETIC_LOGIC_ONLY: synthetic tests demonstrate part or all of the item's logic; not passed.
- LIVE_EVIDENCE_UNDER_REVIEW: separately authorized live evidence recorded and awaiting independent review; not passed.
- PASSED: every assertion in the item has recorded evidence at the level the evidence rules require, verified by a reviewer other than the implementer.
- BLOCKED: required evidence cannot be obtained until a named blocker clears; the record names the separate unblock task.

Acceptance status is distinct from BACKLOG ticket status (OPEN/IN_PROGRESS/VERIFIED/BLOCKED): one records evidence for an A-ID, the other delivery of a ticket, neither is inferred from the other, and a ticket marked VERIFIED cites the evidence records for the A-IDs, or parts of them, that it delivers.

Evidence record, one per claim:
- A-ID, and the part covered if partial.
- Commit: exact SHA.
- Command and result: exact test command and its exact result.
- Evidence level: synthetic, or live (separately authorized).
- Location: sanitized; no user data, tokens or account/order identifiers.
- Reviewer: not the implementer.

A test that proves part of an item cites its A-ID, for example in the test docstring. A citation is traceability only and changes no status. No existing test cites an A-ID.

## Open questions for the owner
- Which items, beyond supported integrations, need live evidence to reach PASSED, and which can pass on reviewed synthetic evidence.
- Where evidence records are kept.
- Which lines, besides those under a hard dietary restriction, count as sensitive for A05.
- Whether bundled items (for example A13) are split into sub-IDs before the first evidence record.
