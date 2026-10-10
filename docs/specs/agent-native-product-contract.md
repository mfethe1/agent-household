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
