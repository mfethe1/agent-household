# Documentation index

Status authority for every Markdown document under `docs/`. Verified 2026-10-10 against `git log -- <path>` on `main` @ `6f387c0` and GitHub issue state. Where a document's own status line disagrees with this index, this index governs.

Several merged papers carry header or closing status lines written before review and merge, for example "UNREVIEWED / UNEXECUTED", "#58 and parent #9 remain OPEN", "not a repository write" and "No … repository writes … occurred". The four merged papers under `docs/specs/` and `docs/research/` are pinned by SHA-256 or merge commit in other documents and issues (#9, #61), so their bodies are left unedited; their hashes are listed below. Some module docs merged with similar pre-merge wording ("Proposal only", "proposed paper", "external paper proposal only").

No document here closes a backlog ticket or passes an acceptance item. Issues #2–#12 also require `docs/specs/TRACEABILITY.md`; it does not exist yet. Requirement-to-A-ID maps currently live in the papers themselves and in #9 comments.

Kinds: governing contract, proposed model, design paper, module doc, research, audit, index.

| Path | Kind | Origin issue → PR / merge commit | Current status |
|---|---|---|---|
| `docs/ACCEPTANCE.md` | governing contract | initial publication, no PR / `719ba57`; named by program #1 | Every scenario pending. A24 and A25 added by this change, pending review. |
| `docs/TRANSACTION_MODEL.md` | proposed model | initial publication, no PR / `719ba57`; named by program #1 | Proposed model. Its independent review is P0-02 under #2 SPEC-00, which is OPEN. |
| `docs/HOSTILE_CALLBACKS.md` | module doc | #41 → #42 / `144bd2d` | Merged test-only fixtures (`tests/hostile_callbacks.py`). #41 closed (completed). Prerequisite of open #33. |
| `docs/JSON_TREE.md` | module doc | #30, #31 → #32 / `f8e586c` | Merged offline guard (`agent_household/json_tree.py`). #30 and #31 closed (completed). `target_record_title` and `target_module_selection` now import it. |
| `docs/OFFER_EVIDENCE.md` | module doc | #19 → #21 / `0161e1f`, #22 / `649f838` | Merged offline offer schema and quote arithmetic. #19 (SPEC-02 child) closed (completed). Parent #4 SPEC-02 is OPEN. Synthetic only; not live offer evidence. |
| `docs/REAL_CALL_PROBE.md` | module doc | #39 → #40 / `66355e8` | Merged test support (`tests/real_call_probe.py`). #39 closed (completed). Prerequisite of open #33. |
| `docs/TARGET_MODULE_SELECTION.md` | module doc | #46 → #47 / `308d402` | Merged offline selector. #46 closed (completed) 2026-10-09T05:55Z, and #46 comment 6075016937 records six strict-qualified mutants including literal-dead; this index did not re-execute them. Any "qualification remains OPEN" or "#46 … remain OPEN" wording in the doc predates that closure. #33 is OPEN. |
| `docs/TARGET_RECORD_TITLE.md` | module doc | #43 (unblocked by #44) → #45 / `174e06c` | Merged offline single-record collector. #43 and #44 closed (completed). Prerequisite of open #33. |
| `docs/TARGET_TCIN.md` | module doc | #35 → #38 / `118a347` | Merged offline TCIN predicate. #35 closed (completed). Prerequisite of open #33. |
| `docs/TARGET_URL.md` | module doc | #27 → #28 / `332a8e9` | Merged offline URL validator. #27 closed (completed). Parents #25 and #23 are OPEN. |
| `docs/research/receipt-wrangler-license-fit.md` | research | #56 → #57 / `276c023` | Research only; no component adopted. #56 closed (completed). #9 comment 6078967123 records "DELIVERED_RESEARCH_ONLY". Parent #9 SPEC-07 is OPEN. |
| `docs/specs/receipt-review-contract.md` | design paper | #50 → #52 / `06894d4` | Merged contract-only design, recorded on #9 (comment 6077106592) as the accepted receipt-review command/result design. #50 closed (completed). Not `SPEC-07.md`; #9 is OPEN; no implementation. |
| `docs/specs/receipt-upload-extraction-contract.md` | design paper | #53 → #55 / `0026aa2` | Merged contract-only design, recorded on #9 (comment 6078541427). #53 closed (completed). Not `SPEC-07.md`; #9 is OPEN; no implementation. |
| `docs/specs/receipt-draft-seam-contract.md` | design paper | #58 (blocker #59) → #60 / `6f387c0` | Merged contract-only design. #58 and #59 closed (completed). #9 comment 6079742096 records "DELIVERED_CONTRACT_ONLY". Implementation admission #61 and #9 are OPEN. |
| `docs/specs/SPEC-01.md` | design paper | #3 SPEC-01 → this change | Capability matrix draft (this change, pending review). #3 is OPEN; A01 is not passed. |
| `docs/specs/INDEX.md` | index | required by #2–#12 → this change | This index (this change, pending review). |
| `docs/reviews/2026-10-gap-analysis.md` | audit | this change | Audit report: 46 verified and 9 rejected gaps. Not a ticket; closes nothing. |
| `docs/reviews/2026-10-remediation-plan.md` | audit | this change | Remediation plan and dispatch status for the audit (#70–#72, #77–#83 filed). Not a ticket; closes nothing. |

## Pinned paper hashes

SHA-256 of each paper as merged. The review and upload hashes match the pins in `docs/research/receipt-wrangler-license-fit.md`. The review and research hashes match the #9 comments. No SHA-256 pin for the draft seam was found; #61 pins it by merge commit `6f387c0`.

| Path | SHA-256 |
|---|---|
| `docs/specs/receipt-review-contract.md` | `ae3fb1b49ff036eef6e58c52bfc61f22e070799a3fe09e99e4ccb764af143d85` |
| `docs/specs/receipt-upload-extraction-contract.md` | `a072a43e89166fdf02c15d2d53b762aaaebc05c67d32ec40403c2cb8144cf5e6` |
| `docs/specs/receipt-draft-seam-contract.md` | `f088c14687d202aea2e6b10d5818803baf7986b44f16bd5f320be310561e0793` |
| `docs/research/receipt-wrangler-license-fit.md` | `73276ec8434561dddd4a6836eed8a849b3205324e386a22e2a7ea1d3cc150a81` |

## Outside `docs/`

- `GOAL_PROMPT.md`: governing contract.
- `BACKLOG.md`: ticket index, with a crosswalk to issues and merged precursor work.
- `README.md` and `CONTRIBUTING.md`: entry page and contribution rules.
