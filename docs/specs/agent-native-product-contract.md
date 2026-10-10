# Agent-native household product contract

Status: reconciled requirement candidate; implementation and runtime acceptance OPEN.
This contract augments GOAL_PROMPT.md, A01–A23 and SPEC-00–10 without weakening them.

## Product and shared state

One product connects needs, evidence-backed baskets, approvals, orders, receipts,
reviewed expenses, split proposals, participant consents, balances and settlement records.
The agent uses typed permissioned tools on the same durable domain as structured clients.
Chat supplements shopping/money/approval surfaces; it is not a parallel ledger.
Purchase authority, sharing visibility, debt acceptance and settlement confirmation are
separate decisions. Recording a settlement does not execute or prove a money transfer.
Retailer access and participant consent cannot be inferred from product direction.

## Additional requirements

- AN-01 Agent action plane: typed read/write/propose/execute tools, explicit actor/household scope, idempotency, durable action history and revocation. Agent and human actions have the same domain validation and conflict semantics.
- AN-02 Delegation experience: goals such as “restock groceries within my budget” and “review and split this receipt”; visible plan, progress, exceptions, approval inbox and resumable recovery. Ground recommendations in accessible evidence; do not invent stock, price or authority.
- AN-03 Integrated shopping journey: need capture → current supported offers → basket comparison → exact approval → qualified checkout or visibly assisted handoff → order/pickup tracking. Unsupported retailers never show simulated successful ordering.
- AN-04 Integrated money journey: receipt capture/import → reviewed expense → exact split proposal → participant acceptance/dispute → balances → separately confirmed settlement record; refunds/corrections propagate with reconstructible history. Recording settlement is not moving money.
- AN-05 Shopping-to-money continuity: persist provenance-linked need/basket/order/receipt/expense chain, deduplicate imports and expose partial failures. Consent and purchase authority remain distinct.
- AN-06 Household collaboration: scoped membership/roles, shared lists, allocation participants, notifications and actor audit. Synthetic multi-user validation can proceed; actual invitations/enrollment need appropriate authorization. Children/guests never gain inferred financial authority.
- AN-07 iOS application: real persisted workflows on a physical iPhone with build identity, navigation, camera fallback, authentication expiry, background/foreground recovery and accessibility evidence.
- AN-08 Android application: equivalent physical Android qualification; parity of core actions and recovery, not screenshot resemblance alone.
- AN-09 Desktop web: authenticated shopping and money workflows, keyboard/accessibility, responsive desktop layouts, save/reload, concurrent human/agent editing and cross-client synchronization.
- AN-10 Trust and authority UI: actor identity, evidence/freshness, approvals and explicit UNKNOWN/needs-user states; bounded policy controls with expiry/revocation. Agent control does not imply blanket spending, calendar writes, debt acceptance or transfers.
- AN-11 Operational robustness: cross-household isolation, server persistence, retry/conflict handling, sanitized observability, recovery/restore/rollback and no duplicated external actions. Preserve original security acceptance.
- AN-12 Competitive acceptance: compare representative shopping and shared-expense journeys to each named incumbent using declared tasks, setup and failure recovery, active time, corrections, correctness, accessibility and participant comprehension. Claim advantage only with evidence, not aspirational scorecards.

## Connected golden journey and client visual contract

From an empty synthetic household, the agent creates a scoped need; a human edits a
basket and reviews its evidence/unknown costs; exact approval permits only qualified
execution or visibly assisted handoff. Order state and an imported/uploaded receipt
retain provenance. A reviewed reconciled expense yields an exact split proposal;
participants individually accept/dispute. Clients reopen identical explainable balances.
A separately confirmed settlement record and later correction preserve attributable history.
Synthetic order states cannot be labeled live retailer success.

Specify mobile navigation, safe areas, touch targets, camera/file fallback, approval inbox,
agent progress/exceptions and money screens. Specify desktop keyboard-friendly comparison,
receipt/split review, balances and action history rather than stretching a phone screen.
For every screen: empty, loading, saved, stale, denied, error, offline/conflicted and
recoverable states; retain drafts without silently executing purchases/consent on reconnect.
Choose mobile framework after capability evidence; PWA-only final delivery is excluded.

## Execution lanes and evidence boundaries

1. Visual contract and native/desktop architecture: continue #63/#64 and accepted preview.
2. Domain/agent action contract: typed actor/household scope, revisions, idempotency,
   action receipts, bounded delegation, approval and revocation; no live spending authority.
3. Receipt/expense domain: continue #9/#10/#61/#62/#80–82, retain exact integer accounting.
4. Durable authorized backend: reconcile #75/#76/#77–79/#87/#88; unsafe runtime admission
   remains blocked, not weakened to ship a demo.
5. Supported retailer/provenance continuity: continue #3/#8/#11/#66; current required
   retailers remain Costco/Amazon/Target. Compare Instacart without assuming API access.
6. Integrate accepted slices, qualify physical clients/live channels, measure outcomes.

Independent visual and pure domain lanes may progress while runtime security is unresolved.
Every slice declares initial/final state, user journey, AN/A/SPEC IDs, authority, dependency,
owner, verification command/artifact and negative recovery cases. Parent independently
verifies, files bugs, cleans/hardens and integrates; repeat build/verify/clean/harden/integrate.
Local tests, hosted exact-head CI, device, live retailer and product outcome claims are distinct.
No enrollment, purchases, payment transfers, private data or deployment is authorized here.

## Persistent learning, stock and weekly meals (required; unimplemented)

- Persist scoped history, preferences and feedback with provenance, confidence, freshness
  and revocable user control. Distinguish explicit preferences, inferred candidates and
  one-time corrections; users can inspect, correct, forget and override learning.
- Purchase history suggests replenishment, never consumption/depletion or order authority.
  Check pantry/freezer stock, pack sizes, attendance and uncertainty. Explain every proposed
  item, quantity, retailer and substitution from evidence and freshness. Absent/stale history
  is explicit, not fabricated. Forget/revocation prevents reuse and cross-household leakage.
- Authorized hard allergy/diet constraints outrank learned preferences; unresolved ingredient
  evidence blocks safety claims. Inference cannot authorize purchases, relax constraints,
  raise budgets or expand private access. Untrusted product/receipt text grants no authority.
- Weekly meals account for ingredients/portions, attendance, preferences, overlapping
  ingredients, replenishment, stock, leftovers and waste reduction. Healthier-eating criteria
  are user-chosen; no prescribed medical diets or claimed medical benefits.
- Remaining all-in budget includes merchandise, tax, delivery/pickup fees, tips, applicable
  membership costs across retailers and reconciled spending. Expose incomplete coverage,
  estimates and unknowns; unknown cost is not zero. Infeasibility produces explicit conflicts
  and bounded alternatives without silently exceeding the ceiling or purchasing.

## Provider-independent action and approval contract

Documented API/MCP contracts let Michael's own agents and available harness assemble carts,
arrange supported fulfillment and perform separately authorized ordering; no required
ChatGPT/Claude gateway. Retailer adapters are separate from models/harnesses, sharing UI
identity, server-side membership/record/attachment permissions, validation, budget, approval,
idempotency, order/receipt status, audit, undo and reconciliation. Test a generic tool client
and chosen available harness for identical authority/recovery, not model-specific success.
Bound delegation by scope, expiry/revocation and revision checks. Exact human approval binds
actor/account/action/payload/version/amount or ceiling/fulfillment/expiry; material change
invalidates it. Persist attempts/idempotency before external effects and reconcile UNKNOWN
before retry. No duplicate orders/imports/ledger/calendar effects or inferred debt consent.

Required Costco/Amazon/Target paths are qualified by operation/channel/geography, distinguishing
genuine ordering APIs, cart/shoppable links, manual handoffs and unavailable access. Official
developer/AI-agent documentation is not live qualification or coverage proof. New Instacart
access remains BLOCKED without verified existing approval; no bypass/signup/outreach or MVP
dependency. Restaurant receipt sharing is included; restaurant ordering is excluded.
One existing pickup-first fulfillment groundwork lane compares eligible staged courier and
accessible Shop&Deliver/Pick&Pack without building a network or payment processor. Indianapolis
is research only; merchant/courier eligibility, cold chain and access remain unverified.

## Traceability and admission

Learning/stock/meal requirements extend AN-02/03/05/10/12, A02/03/05/17/18/19/21 and
SPEC-02/03/04/05/09; action parity extends AN-01/10/11 and SPEC-00/01/05/10.
They augment, never waive, A01–A23, SPEC-00–10, AN-01–12 and original consent/security gates.
The six exact-build gates in docs/ACCEPTANCE.md are mandatory; none is passed by publication.
Existing #63's PWA proposal is an interim scope, superseded only as a final-client destination
by native AN-07/08. #64's bounded authoring recovery and original full coverage remain.
Reuse CLOSED #75's accepted narrow paper evidence; full backend admission is still OPEN.
#76/#87/#88 retain source-bound security prerequisites and cannot be closed by this contract.
Transport work must not monopolize delivery: admitted pure domain/manual receipt/visual work
may progress independently, never falsely labeled authenticated runtime or live ordering.
