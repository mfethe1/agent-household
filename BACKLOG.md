# Delivery backlog

Status: partial implementation exists, not a delivered product. Main c0d685e9 includes pure offer/Target logic, synthetic transient mobile preview and enforced CI. PRs #93/#91 and issues #92/#89/#90/#94 establish CI/preview scope only; authenticated durable backend, live retailer, native devices and integrated money remain open. Historical items below remain OPEN unless independently evidenced in their canonical GitHub issue.

## Phase 0 — prerequisites
- P0-01 OPEN: qualify required retailer/channel capability matrix (A01); owner unassigned.
- P0-02 OPEN: independently review transaction/consent model and financial invariants; owner unassigned.
- P0-03 OPEN: select minimal architecture, self-hosting/storage strategy and phone visual contract; owner unassigned.
- P0-04 OPEN: threat model and privacy/retention/key-recovery specification (A18–A21); owner unassigned.
- P0-05 OPEN: inspect reusable planner/OCR/ledger components and license compatibility; do not import private runtime data/history; owner unassigned.

## Independent receipt-sharing track
- E1 OPEN: upload → evidence retention → reconciled draft, with source/user association (A09–A11); depends P0-02/03/04.
- E2 OPEN: reviewed split → explicit consent → explainable balances (A13–A15/17); depends E1.
- E3 OPEN: refunds/corrections/settlement records (A14/16); depends E2.
- E4 OPEN: authorized source ingestion/checkpoints/revocation (A12/21); depends E1 plus connector qualification.

## Shopping track
- S1 OPEN: one retailer basket/approval/mobile handoff (A02–A07); depends P0-01/02/03/04.
- S2 OPEN: remaining required retailers, qualified channels and cross-store comparison; depends S1.
- S3 OPEN: fulfillment/receipt/charge/refund correlation (A08); depends S1/E1.

## Release track
- R1 OPEN: multi-user authorization/adversarial tests/accessibility (A18/19/22); depends applicable features.
- R2 OPEN: self-hosted setup/export/backup/restore/deletion (A20/21/23); depends storage and ledger.
- R3 OPEN: predeclared measured pilot and operator guide; depends accepted vertical slices.

## External qualification blockers — distinct tasks
- B-RETAILER-ACCESS OPEN: consumer cart/handoff/order/receipt access for each required channel is unverified in this public project. Unblock with authorized source evidence and real compatibility test. Owner integration lead, unassigned. Does not block E1–E3.
- B-INGESTION-ACCESS OPEN: supported itemized account sources unspecified/unverified. Unblock with source contract and authorized import. Owner integration lead, unassigned. Photo upload remains independent.
- B-PARTICIPANT-CONSENT OPEN: real multi-user enrollment/consent is not authorized by publication. Unblock only through participants' scoped enrollment/consent. Owner deployment operator. Synthetic isolation tests may proceed.

## Status protocol
OPEN → IN_PROGRESS → VERIFIED, with BLOCKED flagged separately and a named unblock task. Record DID / NEXT / NEED, exact commit and evidence. Specification publication closes no product ticket.

## Current integrated product delivery queue

Source: current human mandate in GOAL_PROMPT.md and AN-01–12 product contract.
Parent owner: Airy/Hermes, originating Telegram thread 202308. Implementation owners
must hold isolated worktree leases before dispatch; review/closure stays with parent.
GitHub #1 tracks the program; do not duplicate #63/#64 or #75/#76/#87/#88.

- AN-DESIGN OPEN: unified mobile/desktop visual contract and connected golden journey.
  Depends on product contract; no live credentials or transport proof needed. Final state:
  specified structured shopping, receipt, money and approval surfaces with recovery states.
- AN-ACTION OPEN: typed agent tools and shared domain/action receipts, revision/idempotency
  contracts. Depends on product contract and retained consent/security contracts. Final state:
  source-reviewed contracts and synthetic action tests, not authorized live execution.
- AN-CLIENT OPEN: architecture/capability decision for native iOS/Android plus desktop;
  continue #63/#64; preview #89/#90 is accepted only as an interim synthetic surface.
- AN-DURABLE OPEN: authenticated durable vertical slice and one real agent tool mutation.
  Reconcile #75/#76/#87/#88, #77–79; no multi-user release until retained security gates pass.
- AN-EXPENSE OPEN: receipt-to-reviewed-split domain slice, consent and balances.
  Continue #9/#10/#61/#62/#80–82; synthetic deterministic contracts may progress independently.
- AN-CONTINUITY OPEN: link shopping/order/receipt/expense provenance without inferred debt.
  Continue #8/#11; integrate only accepted domain slices and preserve partial-failure states.
- AN-LIVE OPEN: supported grocery-first retailer lane; continue #3/#66 and existing access
  blockers. Required Costco/Amazon/Target remain; Instacart is a comparator/qualification
  candidate, not silently added as an authorized integration or replacement.
- AN-QUALIFY OPEN: physical iPhone/Android, cross-client recovery, accessibility, isolation,
  restoration and predeclared competitive outcomes. Depends on delivered applicable slices.

Each child ticket names AN/A/SPEC IDs, user journey/screen, initial/final durable state,
agent authority, dependencies, one owner and independent verification. Local contract
publication is not product acceptance. Unresolved transport gates stay open, but do not
prevent admitted isolated visual/domain work. No purchase, enrollment, credential,
deployment or payment authority is granted by this queue.
