# Acceptance and evidence matrix

All full-product scenarios below require source-bound evidence. A written requirement is not a passing test. Accepted interim preview/CI slices do not imply full-product acceptance.

## Retailers and shopping
- A01: Costco/Amazon/Target per-channel capability matrix includes documented versus live-tested distinctions and unsupported operations.
- A02: Exact product/seller/pack/quantity/local fulfillment and fresh dietary-label evidence; unsafe/unknown match blocked.
- A03: All-in basket comparison exposes unknown costs and usable-unit/waste assumptions.
- A04: Pre-existing cart lines preserved; concurrent user edit invalidates stale proposal; simultaneous restock drafts do not cause duplicate purchases.
- A05: Expired approval, changed price/slot/seller/quantity and unwanted subscription mode block submission.
- A06: Real phone handoff per required retailer preserves reviewed basket; user completes checkout only under separate exact approval.
- A07: Lost confirmation/crash produces UNKNOWN; authoritative order reconciliation prevents duplicate submission.
- A08: Split shipment, weighted item, substitution, partial cancellation and later return reconcile order/receipt/charge separately.

## Receipt capture and shared expenses
- A09: Phone image/digital multi-page receipt retained with original provenance, selected owner/uploader and separately recorded payers.
- A10: Low-confidence OCR and mismatched totals require correction; pre-tip bill is not presented as final restaurant spend.
- A11: Reimport plus photo upload plus revised receipt do not double-count; two legitimate identical purchases remain distinct.
- A12: Supported account source genuinely imports receipts; transaction-only source labeled incomplete; expired token/sync gap visible and upload fallback works.
- A13: Equal/percentage/fixed/item splits reconcile exactly, including deterministic rounding, shared dishes, taxes/tips/fees/discounts, multiple payers, cash and gift cards.
- A14: Unknown payer or unpaid remainder remains explicit; no fabricated paid amount.
- A15: Proposal, acceptance, dispute, member departure and guest identity claim tested; nonconsenting party is not silently assigned accepted debt.
- A16: Settled expense edit creates adjustment; partial refund, settlement reversal and participant-confirmed settlement preserve audit history.
- A17: Gross budget spend, net allocated cost and outstanding/received reimbursement remain separate; cross-currency netting rejected without explicit conversion.

## Security, recovery and experience
- A18: Negative user/group/guest authorization tests cover records, attachments, exports and agent tools, including shared retailer accounts.
- A19: Malicious receipt/product text cannot authorize actions; unsafe file/oversize upload rejected; model processing disclosure shown.
- A20: Backup restored into isolated environment rebuilds identical ledger projections and attachments; no secrets in logs/public artifacts.
- A21: Unlink/revocation, export, retention/deletion and backup expiry verified against published policy.
- A22: Phone/keyboard/screen-reader flows for upload, corrections, item allocation, approval and disputes; interrupted draft recovers.
- A23: Fresh self-hosted installation follows documented steps; missing integrations fail explicitly, not via seeded fake availability/debts.

## Pilot protocol (provisional thresholds; freeze before pilot)
Compare the same operator's manual workflow with system-assisted workflow on consented tasks of comparable complexity. Record task mix, sample size, failures and uncertainty; no general claim from a single demo.
- Aim for at least 25% lower median active user time for receipt-to-reviewed-split and basket preparation, measured separately; report review/correction time, not just agent runtime.
- Zero unapproved purchases, duplicate orders, unauthorized disclosures or silently incorrect accepted balances is a mandatory safety gate, not proof of future zero risk.
- Every accepted expense reconciles exactly; uncertain imports remain drafts. Report extraction field accuracy and correction rate separately from accounting reconciliation.
- Report handoff success/failure per retailer/channel, missed/duplicate imports, match corrections, disputes, model/connector costs and maintenance burden.
- Threshold changes after pilot begins require a recorded new protocol; do not tune the success definition after seeing results.

## Evidence rules
Synthetic adversarial fixtures demonstrate logic only. Actual supported integrations require separately authorized live evidence. Public summaries redact user data, tokens and account/order identifiers. Each acceptance item records exact commit, test command/result, evidence location and reviewer. No item marked passed from an implementer's assertion alone.

## Agent-native and client acceptance (additional, all pending)

AN-01–12 are defined in docs/specs/agent-native-product-contract.md and retain A01–A23.
- AN-01/02: exercise one permissioned agent action against durable state; the UI reopens
  its result and action receipt. Test stale revision, retry, revocation and exception recovery.
- AN-03/05: follow need → basket → exact approval → supported order/handoff → linked
  receipt. Unsupported operations remain unavailable; partial failure never fabricates success.
- AN-04/06: reviewed receipt → exact split → participant acceptance/dispute → explainable
  balances → separately confirmed settlement record, including refunds and corrections.
  Nonconsent does not become accepted debt; a record is not a payment transfer.
- AN-07: physical iPhone build identity, persisted workflows, camera/fallback, secure
  sessions, expiry, deep links, background recovery and accessibility evidence.
- AN-08: physical Android equivalent with core-action/recovery parity.
- AN-09: desktop authenticated persisted workflows, keyboard/screen-reader use,
  cross-client synchronization and concurrent human/agent edits.
- AN-10/11: actor/evidence/freshness/UNKNOWN UI; bounded authority with expiry and
  revocation; isolation, idempotency, restore and sanitized observability.
- AN-12: predeclared comparative tasks against both incumbents; report setup, active
  time, recovery, corrections, failures, correctness, accessibility and comprehension.
  Existing 25% active-time aim remains provisional until protocol freeze; no invented wins.

Connected acceptance starts from an empty synthetic household: agent creates a need,
human edits a basket, approved supported execution or explicit assisted handoff is tracked,
a receipt is reviewed and a split proposed, each consenting participant accepts their
obligation, and all clients reopen the same explainable balances. Agent authority,
initial/final persisted states, evidence IDs, failures and recovery must be recorded.
Synthetic paths prove logic only; live retailer and physical-device claims remain separate.
