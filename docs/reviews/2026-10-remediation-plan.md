# Remediation plan — October 2026 gap audit

Companion to [the gap analysis](2026-10-gap-analysis.md) (55 candidate gaps: 46 verified, 9 rejected). In-flight state was read from GitHub on 2026-10-10: `main` at `6f387c0`, 14 merged hermes PRs (#21–#60), every `feature/hermes/*` branch already merged, recent activity limited to #63–#68. This audit's own changes are in PR #69.

## Summary

| Coverage | Gaps | Count |
|---|---|---|
| Fix PR #69 | G03 G06 G08 G09 G10 G31 G32 G33 G34 G35 G36 G42 G43 G44 G45 G48 G49 | 17 |
| Partly covered by existing work | G04 G07 G12 G13 G25 G41 G54 | 7 |
| Conflicts with in-flight work | G01 G02 G05 G11 G15 G18 G26 G27 G28 G30 | 10 |
| Uncovered (no owner) | G14 G16 G20 G21 G22 G23 G24 G29 G37 G38 G39 G53 | 12 |
| Rejected / deferred | G17 G19 G40 G46 G47 G50 G51 G52 G55 | 9 |

**Main finding.** The SPEC-00 parent (#2) has had no activity since 2026-10-07. Every in-flight lane is now deciding SPEC-00 matters for itself, without SPEC-00:
- #63/#64 decide architecture, auth and retention.
- #66 decides adapter authority and token handoff.
- #67 builds the Need shape and plans persistence follow-ons. (Update 2026-10-10 05:31Z: #67 closed after its transient, in-memory preview merged via #73 `a88da54`; the open concern is now its persistence and backend follow-ons, starting with PR #74 on need quantities.)

Meanwhile:
- The receipt lane (#61/#62) is stalled by the 240 s / 399-line admission rules (G11).
- The Target lane (#33/#48/#49) is "BLOCKED internally".

None of the work in flight produces the first task in GOAL_PROMPT, the receipt-to-reviewed-expense slice E1 (G01).

**What #69 fixes:**
- tooling (pyproject, pins, CI)
- status records (BACKLOG crosswalk, INDEX.md, README)
- acceptance extensions (A24, A25)
- the SPEC-01 draft
- test hardening on the merged helpers

**What #69 does not fix:** any of the decision-level gaps.

## Conflicts with in-flight work

| Issue(s) | Gaps | Conflict | Sequencing change |
|---|---|---|---|
| #61, #62 | G11, G53, G16, G20, G34, G08 | #62 re-dispatches under the same rules that already timed out: 240 s deadline, ≤399 lines, "reject admission" if coverage cannot fit. Fixture line counting is undefined; the joint-maximum case alone is about 2,420 lines. The pinned seam contract has five oracle ambiguities (G53 a–e), and (d) is an unkillable equivalent mutant. The S01–S03 evaluator risks becoming the de facto RECONCILED/expense rule. #61's gate list uses absolute host paths and an external config. | **Freeze #62 re-dispatch** until (1) the owner rules on size and fixture counting (#70 D-008/D-009), and (2) the allocation reviewer has ruled on each of G53 (a)–(e). Mark #61 as research off the E1 critical path (G01). After #69 merges: re-pin the base SHA and test count, add `research/` to the include list, and log evidence as SYNTHETIC_LOGIC_ONLY. |
| #63, #64 | G02, G26, G27, G28, G30, G18, G24, G31 | #64 Part A (architecture, identity, storage) and the #63 auth/session/retention items decide SPEC-00 and P0-03/P0-04 content inside a mobile paper. #2 claims the same decision. Parts A–D must be "reviewed together", which couples the backend decision to the visual contract. The Part D inventory is frozen at A01–A23. | **Owner picks one authority** (D-010). Recommended: Part A is the *provisional* P0-03 record feeding #2, reviewable on its own. Part A cites the #77 / #78 children, or marks those items BLOCKED. Part B fixes no resume protocol until #80 defines the read surface. Part D inventories A01–A25. No identical 240 s re-dispatch (G11). |
| #66 | G05, G03, G25, G28, G32, G41, G15 | #66 adds Instacart and Kroger and makes grocery-first a scope rule; none of this is in GOAL/ACCEPTANCE. Its capability matrix duplicates #3/A01 and lives in hermes-local BUILDOUT_PLAN.md. Next steps would create real OAuth tokens and browser sessions, and an adapter contract (order authority, substitution, auth handoff), before any token-custody, approval-issuance or authorization rule exists. | **Proceed read-only only:** interim token-custody rule (G28 C) and diagnostics outside the worktree (G41). Matrix output goes to SPEC-01.md rows (G03). The item 4 adapter contract waits for #72 (binding list, G15) and #77 (G25, G26). Every route records substitution-control evidence (G32). Instacart and Kroger stay "optional, pending D-001". |
| #67, #68 | G05, G30, G27, G09, G10, G38, G54, G41, G31 | #67 says "explicitly start implementation", but #1 says product implementation is not admitted. It plans "private persistence/backend" as an immediate follow-on before P0-03/P0-04. Its node tests are outside the Python-only CI, and #67 forbids CI edits. The body contains a Telegram user id and host paths. | **Owner records D-006** (non-product preview exception). The transient preview may proceed once #68 admits an executor. No persistence, auth or backend follow-on before #64 Part A and #78 are accepted. #83 adds a `node --test` job after merge. Owner sanitizes the body. |
| #33, #48, #49, #23, #25 | G04, G11, G43, G49 | The lane stopped because of the line cap, not because of a hold decision. Relaxing the cap (G11) would silently resume it. | The owner records the hold (D-004), and any cap change states that it does not resume this lane. Resume only after #24 qualifies the Target source and confirms the three G49 assumptions. The #69 X2 rows become the boundary rows for the #33 matrix. |
| #29 (closed), #1 | G37, G35, G06 | PR #32's "Does not close #29" auto-closed #29, and #69's BACKLOG repeats "#29 closed" as fact. Hermes PR bodies still use negated closing keywords and merge in under a minute. Child allowed-file lists exclude INDEX/BACKLOG, so status records go stale on every merge. | Owner reopens #29 and marks it held. #69 corrects the crosswalk and adds the keyword rule. Hermes adds a post-merge readback step to its process: confirm that every issue meant to stay open is still OPEN, and update INDEX/BACKLOG for every merged child. |
| #3, #24 | G03, G49 | #69 writes `docs/specs/SPEC-01.md`, the path #3 assigns to hermes. The vocabularies differ: #3 uses documented/live-tested/unsupported, GOAL:15 uses four evidence levels. | The #69 draft header says "input to #3; does not close #3 or pass A01". After merge, hermes amends the draft rather than re-authoring it. #24 must confirm the TCIN length, URL grammar and module shape. |

## Work plan

Dispatch: `#N` = existing or filed issue; `fix PR` = #69.

### Phase 0: now (P0)

| # | Gaps | Remedy | Owner role | Acceptance | Dispatch |
|---|---|---|---|---|---|
| 0.1 | G05 G01 G11 G13 G04 G26 G30 G12 | Record the owner decisions D-001…D-012 (below) in a new `docs/DECISIONS.md`, linked from GOAL_PROMPT.md:6 and #1. Sanitize the BUILDOUT_PLAN.md priority section into it. | Owner decides; coordinator commits through a docs PR | DECISIONS.md merged; #1 links it; new hermes issues cite decision IDs | #70 |
| 0.2 | G08 G09 G10 | **Done:** hermes #93 landed the hosted gate on `main` (`check.yml` with SHA-pinned actions and source binding, `pyproject.toml`, `requirements-dev.txt` pinning ruff 0.16.8 / basedpyright 1.38.1; #92 chose not to import #69's version). #69 adopts #93's files unchanged and keeps the CONTRIBUTING "Running checks" section (G10), aligned to #93's commands. **Residual:** add `research` to the include list in the PR that creates it; keep the hard-coded minimum counts current. | Coordinator | Green #93 gate on the #69 head | #93; #69 (docs); residuals → #83 |
| 0.3 | G03 G49 | **Done in #69:** `docs/specs/SPEC-01.md` DRAFT. Every cell is UNKNOWN because this session's egress policy refused all first-party retailer hosts; the draft records candidate first-party sources, per-row live-test tasks, owner decisions and a Target identifier-assumption table. **Next:** a documented pass (Q0) from an environment that can reach the sources; #3's designated writer then amends the draft rather than re-authoring it. | #3 writer | Cells upgraded only with cited first-party pages; no live claims | #3 |
| 0.4 | G02 G01 | Author SPEC-00 part (a): interim decisions for the local E1 slice (local-only, synthetic or operator data, no third-party OCR or model, fixed upload allowlist and limits). This unblocks E1-minimal without waiting for all of P0-02/03/04. | Coordinator files; writer; independent reviewer | Paper merged with a public review record; BACKLOG E1 dependency narrowed to "SPEC-00(a)" | #71 |
| 0.5 | G14 G15 G16 G18(1–2) G21(1) G31 G33 | Review and revise P0-02 in TRANSACTION_MODEL.md. Slice 1: Receipt, Expense, Allocation and Ledger, plus the receipt→expense seam, the create-receipt event, the precedence line, the charge-state rename and the settlement vocabulary. Slice 2: approval binding and material change. | Owner names author and reviewer; coordinator files | Reviewer verdict replaces "requiring review"; GOAL:27, the model, #7 and A05 share one binding list | #72 |
| 0.6 | G26 G25 G24(B) | Default-deny role × object × action matrix for E1/E2. It covers agent delegation (scoped, expiring, revocable, attributed), the system recovery role, approval issuance outside model control, and untrusted connector/receipt content. | Coordinator files; owner decides group roles and the approval channel | No undefined cell; #64 Part A and #66 cite it | #77 |
| 0.7 | G01 G34 G07 | E1-minimal scope addendum (not an edit of the pinned papers), the dependency-ordered tickets E1a–E2c, and `docs/specs/TRACEABILITY.md`. Filed after D-008. | Coordinator | Tickets read back with allowed files, A-IDs and gates; #61 marked parked or off the critical path | #82 |

### Phase 1: next (P1)

| # | Gaps | Remedy | Owner role | Acceptance | Dispatch |
|---|---|---|---|---|---|
| 1.1 | G31 G32 G25(1) G33 G37 G41 G54 G35 G36 G12(a) | **Done in #69:** A01 matrix columns; A02/A05 purchase safety; A09/A13/A16/A17 extensions; A24 (agent/UI mutation safety); A25 (connector resilience); acceptance status vocabulary and evidence template; BACKLOG crosswalk; README; INDEX; narrow `.gitignore` patterns; machine paths removed from module docs. **Residual (follow-up docs PR):**<br>• A05: a changed substitution policy is a material change.<br>• TRANSACTION_MODEL invariants 5 and 8 (#72).<br>• A-ID remap of the pinned papers (R07-02, R07-06, U07-06, S07 → A24) in TRACEABILITY (#82).<br>• BACKLOG: "#29 closed in error by PR #32's negated keyword".<br>• CONTRIBUTING: no negated closing keywords.<br>• `.gitignore`: `.envrc .netrc storage_state*.json .auth/ *.log`.<br>• Widen "A01–A23" in #1–#12. | Fix-PR author; independent reviewer for A13, A16, A17, A24 (money and authorization) | Review record on #69; residuals tracked | #69 + follow-up docs PR |
| 1.2 | G45 G48 G43 G42 G44 | **Done in #69:** five new tests (json_tree fail-closed contract in both directions; per-call probe counting); Target lookalike-host and near-miss identity rows; exact-message guard assertions; Quote invariance across source_kind × label_status, including unavailable stock. Each new check was shown to kill a scratch mutant the previous suite missed. Tests only; no source changes. **Optional:** assertion-killed form of the no-try mutant; `json.JSONDecodeError` for parser cases. | — | 67 tests pass on 3.11 and 3.13 | #69 |
| 1.3 | G21 G22 G24(A) G53(upload/review) | Successor reconciliation paper for the receipt contracts:<br>• receipt/attachment binding and the CAPTURED trigger;<br>• one outcome table and one reason table;<br>• read surfaces QueryTransfer and QueryReceipt;<br>• expiry disposition, liveness and NEEDS_OPERATOR_RECOVERY;<br>• one entity name, ReceiptRevision.<br>Pinned papers stay unedited. | Coordinator files; writer; reviewer; owner rules on the expiry disposition and Σc+U≠T | Every state in exactly one lifecycle; #61 pin unaffected; ≤399 lines | #80 |
| 1.4 | G20 G23 | Receipt fact inventory and a deterministic RECONCILED rule (A10); duplicate counting effect and cluster consistency (A11). | Coordinator; owner decides materiality and attestation | "Applicable line/total facts" resolved; A11 three-source and triangle cases specified | #81 |
| 1.5 | G27 G28(B) | Policy for retention, deletion and member departure, plus encryption, key recovery, backup and linked-account token custody. | P0-04 owner (to be named) | Every data-class row complete; erasure decision recorded; A21 testable | #78 |
| 1.6 | G28(C) G32(3) G25(3) G41(2) G03 G05 | Interim rules for #66: token and browser-session custody; diagnostics outside the worktree; substitution-control column; MCP output treated as untrusted; matrix rows land in SPEC-01.md. | Coordinator posts; owner authorizes | Next #66 update cites SPEC-01 rows and the custody rule | #66 |
| 1.7 | G26 G30 G27 G18(3) G31(4) G24 | #64 Part A as the provisional P0-03 record (pending D-010), cited from the SPEC-00 children. Need lifecycle owner is #4. Part D covers A01–A25. | Owner (D-010); coordinator | Part A independently reviewed on its own; cites the children | #64 |
| 1.8 | G53 G11 G08 G16 G20 G34 | #61/#62: reviewer rulings on (a)–(e) before redispatch; fixture-counting rule; committed gate config; not the expense model; evidence level SYNTHETIC_LOGIC_ONLY. | Coordinator; allocation reviewer | A ruling for each item posted on #61 before the #62 dispatch | #61 |
| 1.9 | G09 G10 G41(3) G36 | CI follow-ons after #93: required status check; ownership of the minimum test counts; private-path guard; secret scanning and push protection; coverage report. | Owner (admin settings); coordinator | Branch protection shows the check; next hermes PR is green before merge | #83 |

### Phase 2: later (P2/P3)

| # | Gaps | Remedy | Owner role | Acceptance | Dispatch |
|---|---|---|---|---|---|
| 2.1 | G37 G35 G06 G09 G54 G38 | Process rules for hermes:<br>• lint PR bodies for negated keywords;<br>• post-merge readback reopens wrongly closed issues and updates INDEX and BACKLOG rows;<br>• merge waits for green CI on the exact head;<br>• no host paths or chat IDs in public text;<br>• refresh the #1 checkpoint. | Coordinator | Next hermes merge shows all of these | #1 |
| 2.2 | G37 G38 G04 | Owner hygiene pass:<br>• reopen #29 (held);<br>• close #20, citing PRs #21/#22;<br>• fold #26 into #25;<br>• link #68 to #13 and keep #13 open;<br>• reply on #62;<br>• sanitize the #67 body;<br>• enable delete_branch_on_merge and delete the 14 merged branches. | Owner | Tracker matches reality | owner action (no issue) |
| 2.3 | G29 G39 | Upload admission, data classification and redaction, processing-destination registry, metadata minimization, SECURITY.md. | P0-04 owner; coordinator | Records mapped to A19/A20 fixtures; SECURITY.md exists before any hosted release | #79 |
| 2.4 | G39(1–2) | Enable private vulnerability reporting, then a one-line CONTRIBUTING.md:11 channel edit. | Owner (admin), then fix PR or a follow-up docs PR | API returns `enabled:true` | owner action |
| 2.5 | G07 | Prose dependencies → ticket IDs; name the blocker dependents (optional, in #69). TRACEABILITY.md acceptance is in #82. | Fix-PR author | Crosswalk has no unexplained mismatch | fix PR (optional) |
| 2.6 | G12(b) G13 | Rewrite CONTRIBUTING as a short process (authority, claim, gates, size and review rules) after D-008, D-009 and D-011. | Coordinator | CONTRIBUTING names the ticket system, claim mechanism and review record | follow-up docs PR |
| 2.7 | G45 G49 G43 | Post-merge notes: Quote offer reference and evaluation time (#4); confirm the three Target assumptions (#24); reuse the X2 rows (#33). | Coordinator | Notes read back | #4, #24, #33 (one line each, when touched) |

## Owner decisions

Answer these on #70; the agreed answers then go into `docs/DECISIONS.md`.

| ID | Topic | Gaps |
|---|---|---|
| D-001 | Instacart: Costco Same-Day channel or optional extra retailer; Kroger status | G05 G03 |
| D-002 | Target retained (lower priority) or retired | G05 G04 |
| D-003 | Grocery-first with opt-in categories as the product default | G05 |
| D-004 | Hold the Target title lane until #24 qualifies a source | G04 |
| D-005 | Calendar writes in or out of scope | G05 |
| D-006 | #67 as a non-product preview exception to #1's gate | G05 G01 |
| D-007 | Executors stop on issue-vs-GOAL conflicts | G05 |
| D-008 | Critical-path order: E1 vs #67 vs #66 | G01 |
| D-009 | Size cap, stacked slices, fixture counting, author-route deadline | G11 |
| D-010 | Single authority for architecture/auth/retention: #2 or #64 Part A | G02 G26 G30 |
| D-011 | Who qualifies as an independent reviewer; record format and location | G13 |
| D-012 | Status authority: issues vs BACKLOG | G06 G12 |

Owner-only GitHub writes and settings:
- reopen #29;
- close #20;
- private vulnerability reporting and secret scanning;
- branch protection;
- delete_branch_on_merge;
- sanitize the #67 body.

## Deferred and rejected

See `docs/reviews/2026-10-gap-analysis.md` for the reasoning behind each.

| Gap | Disposition |
|---|---|
| G17 | Rejected now. Split rounding and pro-rating belong to SPEC-08 (#10) when E2 is specified, not before P0-02. |
| G19 | Rejected now. Refund sign and linkage are owned by #8/#11 (A08/A16). #72 lists refunds under "lifecycles not yet specified". |
| G40 | Rejected. Keep the unanchored .gitignore directory rules; add a comment only when P0-03 storage starts. |
| G46 | Rejected. offer_evidence v1 vocabulary stays as #19 accepted it; P0-01 decides channel structure. |
| G47 | Rejected. Decode edge behaviour is optional hardening, off the critical path. |
| G50 | Rejected as a standalone slice; goes on the #33 wiring checklist (expected_tcin precondition). |
| G51 | Rejected (deferred note). Instrument more dunders only when a subclass-accepting consumer appears. |
| G52 | Rejected now. The inbound-license allowlist stays in P0-05 until a component is proposed; the pinned license paper is unedited. |
| G55 | Rejected now. Freeze pilot thresholds in SPEC-10 (#12) / R3 before any pilot; no E1 instrumentation. |

## Dispatch status

| Item | Status |
|---|---|
| #70 [DECISION] program decision log (D-001…D-012) | filed |
| #71 SPEC-00 interim decisions for the local E1 slice | filed |
| #72 P0-02 transaction/consent model review | filed |
| #77 authorization, visibility and agent-delegation matrix | filed |
| #78 retention, deletion, encryption, keys and token custody | filed |
| #79 upload admission, data classification and SECURITY.md | filed |
| #80 receipt contract reconciliation successor | filed |
| #81 receipt fact inventory and duplicate counting | filed |
| #82 E1-minimal slice, ticket chain and TRACEABILITY.md | filed |
| #83 CI enforcement follow-ons | filed |
| Cross-reference comments on #1, #3, #61, #64, #66 | posted (#67 closed before posting; its points moved to #1 and #64) |
| Hosted CI gate (Python, Ruff, Basedpyright, Node) | landed by hermes in #93; #69 adopts it |

Filed issues are marked "audit dispatch — not admitted": the coordinator admits them under #1's rules after the decisions in #70. Hermes filed #73–#76 meanwhile; #76 (F06 shared authority serialization) is adjacent to #77/#78 and is cross-linked from both.
