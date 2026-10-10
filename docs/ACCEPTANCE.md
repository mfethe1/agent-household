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

## Six finite exact-build completion gates (all OPEN)

These augment every applicable A/SPEC/AN obligation. Record build/source identity, command,
initial/final persisted state, evidence location, one owner and independent verification.
An inventory must distinguish completed foundation from unverified product requirements.
Complete only when all applicable gates pass against the saved exact-build state. Otherwise
record each failed gate, its owner, next bounded action or authorization dependency in the
existing checks/progress; no partial review or prerequisite count substitutes for acceptance.

1. **Baseline/mandate/ownership:** reconcile assets, live issues/PRs and existing mandate;
   save completed-versus-unverified inventory and prioritized acceptance matrix, one owner
   per task/worktree. Preserve accepted work/budget; no restart or duplicate agents.
2. **Two-cycle connected product:** two synthetic household members use actual agent tools
   and human UI on authenticated persistent storage through the full connected journey,
   surviving process restart and client reopen. Every cart line has evidence/quantity rationale.
   Corrections/removals/substitutions persist and change a second cart. Test absent/stale history,
   uncertain stock, one-time/persistent preferences, conflicts, deletion/revocation, budgets and
   allergies. Zero hard-constraint violations, inferred spending authority or cross-household
   learning leakage. Receipt/tax/tip/fee/discount/refund/split accounting reconciles exactly in
   deterministic integer minor units; disputes never become accepted debt.
3. **Clients and tools:** the same journey passes on physical iPhone, physical Android and
   desktop web, recording build/OS, synchronization, accessibility/keyboard, camera-denial
   fallback, expired sessions and interrupted save/upload recovery. Emulation is supporting
   evidence only. Generic documented tool client and Michael's chosen available harness prove
   identical authority/recovery; model-specific success alone fails. Secure sessions, deep
   links, accessible navigation and qualified notifications remain required.
4. **Adversarial/recovery:** independent inventory covers cross-user/household/attachment
   access, revoked/expired authority, hostile content, stale approvals, concurrent edits,
   duplicate/reordered requests, lost responses, crash after external effect, offline replay
   and timeout. Zero unauthorized disclosures/effects or duplicated external/ledger effects.
   UNKNOWN remains blocked until reconciliation. Audit reconstruction, undo/adjustments,
   export, backup restore and rollback pass. No original gate or #87/#88 prerequisite waived.
5. **Retailer continuity:** separately qualify required supported retailer operation/channel/
   geography and order/receipt/refund continuity in the capability matrix. Consequential live
   tests need separate bounded approval. Missing access/device/capability/approval is a named
   blocker, never completion; independent manual receipt/expense work continues.
6. **Weekly meals and outcomes:** demonstrate user-chosen healthier-eating criteria,
   attendance/portions, preferences, stock and total remaining budget. Account for every meal's
   ingredients/portions; explain substitutions with reviewed allergy/diet evidence. All-in cost
   including fees/tax/tips/membership and reconciled prior spending stays within the remaining
   ceiling; expose incomplete coverage and estimates (see the contract's persistent learning,
   stock and weekly meals section). Unknown is not zero. Infeasible
   constraints produce conflicts/alternatives without purchase. Feedback changes the next plan;
   record stock/leftover use and waste choices. Require exact-order approval. Compare declared
   representative shopping/expense tasks against recorded baseline active time, handoffs,
   corrections and understanding: 100% correct approved baskets/receipts/splits, zero unintended
   effects and reduced active work/handoffs. Disclose incumbent advantages, not feature parity.

### Original acceptance case → required gate evidence (all OPEN)

Each row requires every clause of the unchanged A item above, with positive and refusal/edge cases, exact-build initial/final states and independent evidence. Gate numbers reference this document; topic-level coverage alone fails. Record owner, evidence location and unmet dependencies per row in the existing saved inventory; do not assign ownership from this table.
| Case | Required gates | Evidence case that must not be lost |
|---|---|---|
| A01 | 1,5 | Each named retailer/channel's documented/live/unsupported operation matrix. |
| A02 | 2,4,5,6 | Exact seller/pack/quantity/local fulfillment; fresh labels; unknown/unsafe refusal. |
| A03 | 2,6 | All-in comparison with unknown costs and usable-unit/waste assumptions. |
| A04 | 2,4,5 | Existing cart preserved; concurrent edit invalidation; simultaneous drafts cannot duplicate purchases. |
| A05 | 2,4,5 | Expiry and each price/slot/seller/quantity/subscription change block submission. |
| A06 | 3,5 | Actual required-retailer phone handoff, reviewed basket and separate exact checkout approval. |
| A07 | 4,5 | Lost confirmation/crash, UNKNOWN and authoritative reconciliation before retry. |
| A08 | 2,5 | Shipment/weight/substitution/cancellation/return with distinct order, receipt and charge evidence. |
| A09 | 2,3,4 | Actual multi-page image/digital capture; original provenance; owner/uploader/payers distinct. |
| A10 | 2,3 | OCR uncertainty/total corrections and pre-tip versus final restaurant spend. |
| A11 | 2,4 | Reimport/photo/revision dedup versus two legitimate identical purchases. |
| A12 | 3,4,5 | Qualified receipt source; incomplete transaction source; expired token/gap/fallback. |
| A13 | 2,4 | Every listed split/payment mode; rounding and tax/tip/fee/discount conservation. |
| A14 | 2,4 | Unknown payer/unpaid remainder explicit; no fabricated paid amount. |
| A15 | 2,4 | Proposal/acceptance/dispute/departure/guest claim; nonconsent never accepted debt. |
| A16 | 2,4 | Settled edit/partial refund/reversal/participant confirmation; preserved audit. |
| A17 | 2,4,6 | Gross spend/net allocation/reimbursement separate; unauthorized currency netting refused. |
| A18 | 3,4 | Negative record/attachment/export/tool authorization, guests and shared retailer accounts. |
| A19 | 3,4 | Hostile receipt/product text, unsafe/oversize file rejection and processing disclosure. |
| A20 | 4 | Isolated restored ledger/attachments identical; secret-free logs/public evidence. |
| A21 | 4 | Unlink/revocation/export/retention/deletion/backup expiry against published policy. |
| A22 | 3,4 | Phone/keyboard/screen-reader upload/correct/allocate/approve/dispute; interrupted recovery. |
| A23 | 3,4 | Fresh self-hosted install from instructions; missing integrations explicitly fail. |

The provisional 25% aim above is not a substitute for required demonstrated reductions.
Preview/history analysis, local tests, hosted CI, physical devices, live retailer continuity
and measured outcomes are separate claims. Protect identities, schedules, diet/health data
and preferences; public evidence uses synthetic families only. No completion from worker report.
