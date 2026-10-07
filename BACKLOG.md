# Delivery backlog

Status: specification published; implementation not started here. Each ticket needs a named implementation owner and exact scope before work. None are complete.

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
