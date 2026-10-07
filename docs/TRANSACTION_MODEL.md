# Proposed transaction and consent model

Status: design contract requiring review before implementation; not an implemented schema.

## Entities
- User / GuestIdentity / Group / Membership: separate identities and roles; guest obligations provisional. Claim/merge requires review and does not erase provenance.
- Need / Basket / BasketRevision / OfferEvidence: shopping intent, exact proposal and timestamped product evidence.
- Approval: actor/account/channel, immutable basket revision, amount ceiling, expiry and authorized action scope.
- SubmissionAttempt: durable intent, idempotency/correlation key and observed external outcome.
- Order / Fulfillment / OrderLine: one order may have multiple shipments and changed quantities.
- Receipt / ReceiptVersion / SourceAttachment / Extraction: immutable originals and reviewed normalized versions with provenance.
- Charge / Refund: observed payment records with pending/settled/unknown states; never inferred solely from a receipt.
- Expense / AllocationProposal / Acceptance / Dispute: participants, payer contributions, reviewed shares and consent evidence.
- LedgerEntry / Adjustment / SettlementRecord: immutable attributed financial events; projections rebuild from entries.
- ImportSource / ImportCheckpoint / MatchDecision: source authorization, coverage and deduplication evidence.

## Transitions
- Basket: DRAFT → REVIEWED → APPROVED → SUBMITTING → CONFIRMED; FAILED or UNKNOWN are explicit alternatives. New material revision invalidates approval.
- Submission UNKNOWN: authoritative reconciliation → CONFIRMED or proven not submitted; otherwise remain UNKNOWN. No blind retry.
- Receipt: CAPTURED → EXTRACTED → NEEDS_REVIEW or RECONCILED. Original evidence remains intact across corrections.
- Allocation: DRAFT → PROPOSED → ACCEPTED, with DISPUTED/REJECTED alternatives. Partial acceptance must not silently finalize others' obligations.
- Settlement: RECORDED_UNVERIFIED → CONFIRMED_BY_PARTIES when applicable; neither state means bank-verified without supporting source evidence. Reversal is a new entry.

## Invariants
1. Monetary values use integer minor units and explicit currency; conversion requires documented rate/time/approval.
2. Final expense shares equal reviewed distributable total exactly. Payer contributions plus documented unpaid amount reconcile to that total; do not force an unpaid bill to appear paid.
3. Each adjustment preserves original entries and actor/reason/time; settled history is not overwritten.
4. No upload or group membership alone creates an accepted debt.
5. Agent/user cart changes use optimistic revision checks and ownership metadata.
6. Source deduplication includes source identifiers and version lineage; image hashes are useful evidence, not a complete duplicate oracle.
7. Import confirmations, receipts and charges may refer to one purchase without being the same event. Multiple identical purchases remain possible.
8. Gross spending, personal cost and reimbursement projections are distinct and explainable.
9. Every attachment, expense and tool mutation receives server-side authorization; UI hiding is not access control.
10. External action and local commit cannot be assumed atomic. Persist intent, record outcome, reconcile on recovery.

## Decisions requiring review
Select posting/consent workflow, group roles, deletion/backup retention rules, encryption/key recovery, token storage and supported ingestion sources before their implementation. Defaults in GOAL_PROMPT.md are proposed conservative behavior, not evidence of participant agreement.
