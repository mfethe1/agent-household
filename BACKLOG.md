# Delivery backlog

Status: specification stage. Offline synthetic precursor primitives (`agent_household/`, `tests/`) and contract-only design papers are merged (see "Merged precursor work"); they close no ticket. No backlog ticket or acceptance item is complete, and product implementation is not yet admitted (#1). GitHub issues are the detailed live plan; the crosswalk below maps each ticket to them. Each ticket needs a named implementation owner and exact scope before work.

Owners: issues #1–#12 name program roles only. Airy coordinates and accepts; Mack is the designated writer in isolated worktrees. #2 records "Owner/reviewer: unassigned". Per-ticket implementation owners stay unassigned until the coordinator names them.

## Phase 0 — prerequisites
- P0-01 OPEN: qualify required retailer/channel capability matrix (A01); owner unassigned.
- P0-02 OPEN: independently review transaction/consent model and financial invariants; owner unassigned.
- P0-03 OPEN: select minimal architecture, self-hosting/storage strategy and phone visual contract; owner unassigned.
- P0-04 OPEN: threat model and privacy/retention/key-recovery specification (A18–A21); owner unassigned.
- P0-05 OPEN: inspect reusable planner/OCR/ledger components and license compatibility; do not import private runtime data/history; owner unassigned.

## Independent receipt-sharing track
- E1 OPEN: upload → evidence retention → reconciled draft, with source/user association (A09–A11); depends P0-02/03/04; owner unassigned.
- E2 OPEN: reviewed split → explicit consent → explainable balances (A13–A15/17); depends E1; owner unassigned.
- E3 OPEN: refunds/corrections/settlement records (A14/16); depends E2; owner unassigned.
- E4 OPEN: authorized source ingestion/checkpoints/revocation (A12/21); depends E1 plus connector qualification; owner unassigned.

## Shopping track
- S1 OPEN: one retailer basket/approval/mobile handoff (A02–A07); depends P0-01/02/03/04; owner unassigned.
- S2 OPEN: remaining required retailers, qualified channels and cross-store comparison; depends S1; owner unassigned.
- S3 OPEN: fulfillment/receipt/charge/refund correlation (A08); depends S1/E1; owner unassigned.

## Release track
- R1 OPEN: multi-user authorization/adversarial tests/accessibility (A18/19/22); depends applicable features; owner unassigned.
- R2 OPEN: self-hosted setup/export/backup/restore/deletion (A20/21/23); depends storage and ledger; owner unassigned.
- R3 OPEN: predeclared measured pilot and operator guide; depends accepted vertical slices; owner unassigned.

## External qualification blockers — distinct tasks
- B-RETAILER-ACCESS OPEN: consumer cart/handoff/order/receipt access for each required channel is unverified in this public project. Unblock with authorized source evidence and real compatibility test. Owner integration lead, unassigned. Does not block E1–E3.
- B-INGESTION-ACCESS OPEN: supported itemized account sources unspecified/unverified. Unblock with source contract and authorized import. Owner integration lead, unassigned. Photo upload remains independent.
- B-PARTICIPANT-CONSENT OPEN: real multi-user enrollment/consent is not authorized by publication. Unblock only through participants' scoped enrollment/consent. Owner deployment operator. Synthetic isolation tests may proceed.

## Issue crosswalk
Ticket-to-issue mappings come only from each issue's own "Existing backlog" line, and issue A-IDs from its "Acceptance" line (read 2026-10-10). "Ticket A-IDs" are this file's.

| Ticket | Issue / SPEC | Ticket A-IDs | Issue acceptance line | Status |
|---|---|---|---|---|
| P0-01 | #3 SPEC-01 | A01 | A01 | OPEN; Target precursors via #23 (below) |
| P0-02 | #2 SPEC-00 | — | A18–A23 where applicable | OPEN |
| P0-03 | #2 SPEC-00 | — | A18–A23 where applicable | OPEN |
| P0-04 | #2 SPEC-00 | A18–A21 | A18–A23 where applicable | OPEN |
| P0-05 | #4 SPEC-02 ("P0-05 reuse review") | — | A02/A03 | OPEN |
| E1 | #9 SPEC-07 | A09–A11 | A09–A11/A18/A19/A22 | OPEN; contract-only papers and research merged (below); implementation admission #61 OPEN |
| E2 | #10 SPEC-08 | A13–A15/A17 | A13–A15/A17/A18 | OPEN |
| E3 | #11 SPEC-09 | A14/A16 | A16/A17/A20 | OPEN |
| E4 | #12 SPEC-10 | A12/A21; A25 † | A12/A18–A23 and predeclared pilot | OPEN |
| S1 | #4 SPEC-02 (read-only precursor); #7 SPEC-05 | A02–A07; A25 † | #4: A02/A03; #7: A04–A07/A22 | OPEN; offer and Target precursors merged (below) |
| S2 | #7 SPEC-05 | — | A04–A07/A22 | OPEN |
| S3 | #8 SPEC-06 | A08 | A08/A14/A17 | OPEN |
| R1 | #12 SPEC-10 | A18/A19/A22; A24 † | A12/A18–A23 and predeclared pilot | OPEN |
| R2 | #12 SPEC-10 | A20/A21/A23 | A12/A18–A23 and predeclared pilot | OPEN |
| R3 | #12 SPEC-10 | — | A12/A18–A23 and predeclared pilot | OPEN |
| B-RETAILER-ACCESS | #3 SPEC-01 | — | A01 | OPEN |
| B-INGESTION-ACCESS | #12 SPEC-10 | — | A12/A18–A23 and predeclared pilot | OPEN |
| B-PARTICIPANT-CONSENT | none states it | — | — | OPEN |

† Added by this change, pending review; no issue states these mappings yet. A24 (agent and UI mutation safety) maps to R1 and is also a cross-cutting requirement of every ticket whose slice adds a mutating command, tool or UI action. A25 (connector resilience) maps to S1 and E4.

Issues with no backlog ticket: #5 SPEC-03 (optional decision layer; strengthens A02/A19), #6 SPEC-04 (whole-basket optimization and phone review; A03/A22), #63 MOBILE-01, #67 MOBILE-F01 (closed: transient preview merged via #73, `a88da54`) and #66 (grocery-first retailer qualification). The Target observation chain (#23, #25, #33; #29 closed) sits under #3 and #4, per #23. Open blocker and unblock issues are tracked only on GitHub: #13–#18, #20, #24, #26, #48, #49, #62, #64, #65, #68.

## Merged precursor work
Every row is offline and synthetic, contract-only or research-only. None is live retailer evidence, and none credits an acceptance item.

| PR | Merge commit | What it is | Issue served | Status |
|---|---|---|---|---|
| #21 | `0161e1f` | `offer_evidence`: bounded offline offer schema | #19 (SPEC-02 child of #4) | synthetic precursor; closes no ticket |
| #22 | `649f838` | `offer_evidence`: fail-closed quote arithmetic | #19 (closed) | synthetic precursor; closes no ticket |
| #28 | `332a8e9` | `target_url`: strict Target product URL validator | #27 (closed); parents #25, #23 OPEN | synthetic precursor; closes no ticket |
| #32 | `f8e586c` | `json_tree`: bounded already-decoded JSON tree guard | #30, #31 (closed) | synthetic precursor; closes no ticket |
| #37 | `5c5f190` | Formatter baseline restored for `offer_evidence` and its tests | #36 (closed; blocker for #35) | formatting of a synthetic precursor; closes no ticket |
| #38 | `118a347` | `target_tcin`: exact Target TCIN predicate | #35 (closed); prerequisite of #33 | synthetic precursor; closes no ticket |
| #40 | `66355e8` | `tests/real_call_probe.py`: real-call trace regression support | #39 (closed); prerequisite of #33 | synthetic precursor; closes no ticket |
| #42 | `144bd2d` | `tests/hostile_callbacks.py`: hostile callback fixtures | #41 (closed); prerequisite of #33 | synthetic precursor; closes no ticket |
| #45 | `174e06c` | `target_record_title`: single-record raw-title collector | #43, #44 (closed); prerequisite of #33 | synthetic precursor; closes no ticket |
| #47 | `308d402` | `target_module_selection`: bounded title-module selector | #46 (closed); #33 OPEN | synthetic precursor; closes no ticket |
| #52 | `06894d4` | `docs/specs/receipt-review-contract.md` | #50 (closed) under #9 | contract-only; closes no ticket |
| #55 | `0026aa2` | `docs/specs/receipt-upload-extraction-contract.md` | #53 (closed) under #9 | contract-only; closes no ticket |
| #57 | `276c023` | `docs/research/receipt-wrangler-license-fit.md` | #56 (closed) under #9 | research only; nothing adopted; closes no ticket |
| #60 | `6f387c0` | `docs/specs/receipt-draft-seam-contract.md` | #58, #59 (closed) under #9 | contract-only; closes no ticket |
| #73 | `a88da54` | `preview/`: transient local mobile needs preview (in-memory only) | #67 (closed) under #63 | local preview; not M0, closes no ticket |
| #74 | `90428e6` | `preview/`: need amount intent (quantity, units, package) | #63 | local preview; not M0, closes no ticket |

Document status and pinned hashes: [docs/specs/INDEX.md](docs/specs/INDEX.md).

## Open questions for the coordinator
- Whether precursor work moves P0-01, S1 or E1 to IN_PROGRESS. This file keeps every ticket OPEN.
- Whether #5, #6, #63, #66 and #67 get backlog tickets.
- Which record governs when this file and an issue disagree. GOAL_PROMPT.md says to "update backlog and evidence" after each slice.
- Named implementation owner for each ticket.

## Status protocol
OPEN → IN_PROGRESS → VERIFIED, with BLOCKED flagged separately and a named unblock task. Record DID / NEXT / NEED, exact commit and evidence. Specification publication closes no product ticket.
