# SPEC-07 Receipt Review Command Contract — Design Paper for #50

## 1. Status, custody, and scope
- Status: fresh, complete, local design proposal; not an accepted specification or implementation.
- Baseline reference: `308d40212ac530942c02c42e2e3db012d971eb3c`.
- Proposed future publication: `docs/specs/receipt-review-contract.md`.
- Approved author route: `openai-codex/gpt-6.1-sol`; tools disabled.
- This paper uses supplied TASK and transaction-model excerpts; source custody and omitted source documents remain independently unverified.
- No network, private data, execution, installation, source lease, repository writes, runtime changes, or publication occurred.
- Airy owns coordination/acceptance; an independent reviewer must assess the complete contract.
- Phone UI and agent tools consume one future backend contract; transport and architecture remain undecided.
- #50 is independent of blocked Target observer work #49/#48/#33 and does not close parent #9.
- #51 solved artifact delivery is not reopened by rejection of a design candidate.
- Normative requirements below describe future behavior, not existing guarantees.
- Public publication gate remains **≤399 canonical additions plus deletions**, unchanged.
- Local paper length is not publication admission; coverage must not be trimmed to pass that gate.

## 2. Evidence and receipt invariants
- Originals are immutable evidence: identity, source version, provenance, page order, and original coordinates survive every correction.
- A reviewed revision adds normalized facts and references; it never rewrites an original attachment or extraction.
- Extraction is untrusted draft data, including OCR text, suggested values, confidence, missing facts, and uncertainty.
- OCR success establishes neither an accepted expense, a paid charge, final spend, nor an accepted liability.
- Receipt owner, attachment uploader, authenticated command actor, and asserted payer are separate identities.
- Receipt text cannot supply executable commands, actor identity, authorization, permissions, or trusted provenance.
- Every attachment/evidence read, receipt mutation, operation query, and agent output requires current server-side authority.
- SPEC-00 defines that authority; roles, sharing semantics, hosting, retention, deletion, and key recovery remain blocked.
- Preserving originals within this contract does not establish perpetual retention or override future authorized deletion policy.
- Recovery, export, and deletion must reference SPEC-00; conflicts between custody and deletion remain unresolved.
- Receipt review does not allocate shares, accept debt, process payments, perform checkout, or merge accounting events.
- Existing charge/refund evidence remains distinct from receipt review and cannot be inferred from receipt arithmetic.

## 3. Data matrix
| Record | Required contract fields | Preservation / interpretation |
|---|---|---|
| SourceAttachment | attachment ID, namespaced source ID/version, provenance, ordered page IDs | Preserve original content identity and ordering. |
| SourceEvidence | source version, page ID, original coordinate space and region, evidence kind | Corrections retain original references; transformed views require explicit mappings. |
| Extraction | extraction ID/version, attachment references, draft fields, uncertainties, absent facts | Untrusted and immutable; confidence does not establish truth. |
| ReceiptRevision | receipt ID, immutable revision ID, predecessor, actor/reason/time, reviewed fields, evidence | New revision preserves history and original source versions. |
| ReviewFacts | currency, final total, finality, required material facts, contributions, explicit unpaid | Unknown and absent are explicit; no fabricated defaults. |
| Contribution | payer reference or explicit unknown payer, integer amount, currency, evidence | Unknown attribution retains evidence and blocks reconciliation. |
| DuplicateEndpoint | receipt ID, expected review revision, designated source ID/version | Both distinct endpoints are mandatory, including source-version binding. |
| MatchDecision | immutable ID, exact endpoint pair/source versions, disposition, evidence, predecessor | Reversal is a new decision, not deletion or endpoint substitution. |
| OperationIntent | authenticated actor, operation ID, command, original canonicalization version, full binding, digest | Immutable original reservation; retry payload cannot recreate it. |
| OperationEvidence | reservation/fence evidence, effect proof, terminal-existence proof, immutable outcome if present | Effects and terminal outcomes are separate proof dimensions. |
| OperationOutcome | APPLIED, CONFLICT, or INVALID; original binding reference; permitted result details | Immutable once established; retry errors cannot overwrite it. |

## 4. Review validity and money bounds
- Receipt states are CAPTURED, EXTRACTED, NEEDS_REVIEW, and RECONCILED; revisions remain immutable.
- RECONCILED requires all required material facts to be present, sufficiently evidenced, and mutually consistent.
- Required facts include explicit supported currency, final purchase total, finality, applicable line/total facts, and complete payer/unpaid accounting.
- Material uncertainty about pre-tip status, finality, currency, amount, or payer attribution independently prevents RECONCILED.
- Optional unknown facts are eligible only when explicitly classified as nonmaterial to identity, finality, totals, attribution, and duplicate certainty.
- Merchant display decoration or nonmaterial OCR text may remain unknown; optional classification cannot conceal a material uncertainty.
- A supported currency must have explicit minor-unit metadata and implementation-approved bounds; these are not selected here.
- For a supported bound `B`, require integer minor-unit total `T`, contributions `cᵢ`, and explicit unpaid `U`.
- Require `0 ≤ T ≤ B`, `0 ≤ cᵢ ≤ T`, `0 ≤ U ≤ T`, and exact integer conservation `Σcᵢ + U = T`.
- Intermediate accumulation must remain bounded; floating arithmetic, implicit rounding, conversion, or silent overflow is forbidden.
- Unknown currency or amount does not mean zero; missing unpaid does not mean paid.
- A zero-total purchase is eligible only with explicit final zero evidence, zero contributions, zero unpaid, and all other required facts established.
- Overpayment, negative unpaid, out-of-bound values, and conservation mismatch make a reconciliation command INVALID.
- Negative purchases, refunds, signed contributions, and netting are unsupported by this purchase-only contract.
- Unsupported reconciliation preserves original, draft, contribution, and refund evidence; it does not erase or reinterpret them.
- A known contribution amount with unknown payer remains evidence but yields NEEDS_REVIEW, never an invented unpaid amount.
- Valid arithmetic cannot close attribution review; unresolved material facts likewise remain NEEDS_REVIEW.
- ReconcileReview may record an honest NEEDS_REVIEW revision; it may not assert RECONCILED while a required issue remains.

## 5. Duplicate dispositions and evidence predicates
| Disposition | Necessary reviewed predicate | Insufficient alone |
|---|---|---|
| SAME_SOURCE_VERSION | Authenticated namespaced source identity and equal authoritative source version | Equal attachment hash, OCR text, or filename |
| REVISED_SOURCE_LINEAGE | Authenticated namespaced predecessor/successor linkage between designated versions | Similar content, later timestamp, or changed total |
| SAME_PURCHASE | Authenticated namespaced purchase-event evidence tying both sources to one purchase | Same merchant/time/amount or fuzzy similarity |
| DISTINCT_PURCHASES | Authenticated namespaced purchase-event evidence establishing distinct purchases | Different hashes or assumed independence |
| UNRESOLVED | Required predicate unavailable, conflicting, unqualified, or ambiguous | A candidate score cannot establish certainty |
- Trusted issuer, authenticated ingestion, namespace, and lineage qualifications depend on unaccepted SPEC-00 decisions.
- Until qualifications are accepted and satisfied, apparent authoritative evidence is not elevated to reviewed certainty.
- Hashes and fuzzy matching may propose candidates; they never auto-merge receipts, purchases, expenses, or charges.
- Photo/import ambiguity remains UNRESOLVED unless a disposition’s full evidence predicate is established.
- Every proposal, resolution, and reversal binds both distinct receipts, designated source versions, expected revisions, and authority.
- Root receipt ID/revision must equal a designated endpoint exactly; no third receipt is ignored or implicitly included.
- Proposal and prior-decision IDs must resolve to their immutable exact pair and source versions.
- Reversal references the prior decision and appends a new decision with retained provenance and reason.
- Both endpoints are validated and committed atomically; a failure on either leaves neither endpoint partially updated.

## 6. Command and binding matrix
| Command | Additional payload | Effect |
|---|---|---|
| ProposeCorrection | field changes, evidence references, uncertainty, reason | Append draft/review revision; do not fabricate acceptance. |
| ReconcileReview | reviewed facts, finality, contributions, explicit unpaid, evidence | Append NEEDS_REVIEW or eligible RECONCILED revision. |
| ProposeDuplicateLink | both endpoints, candidate evidence | Append exact-pair candidate; no accounting merge. |
| ResolveDuplicateLink | proposal ID, both endpoints, disposition, qualifying evidence | Append immutable exact-pair decision. |
| ReverseDuplicateDecision | prior decision ID, both endpoints, reason, replacement disposition/evidence | Append reversal/new decision; retain prior history. |
| QueryOperation | authenticated actor/operation reference | Read proven status after current authorization; no mutation payload comparison. |
- Every mutation includes actor reference, receipt ID, expected revision, operation ID, and command kind.
- Authenticated identity must match the actor reference; the client cannot choose another actor’s operation namespace.
- The immutable full binding includes all mutation semantics: root, expected revisions, both endpoints when applicable, source versions, referenced IDs, facts, evidence references, and reason.
- Original canonicalization version and canonical command digest are persisted with that binding; no digest algorithm is invented here.
- Semantically relevant content cannot be excluded from comparison; a digest is not a substitute for recoverable binding evidence.
- Exact retry comparison uses the original canonicalization version, never the latest version.
- Unavailable original canonicalization yields comparison-blocked UNKNOWN, not false reuse, false INVALID, rebinding, or permission for a new ID.
- An established status query needs no command payload or canonicalizer; it requires proven operation identity/outcome and current authorization.

## 7. Admission, lifecycle, and recovery
- Authority denied or unavailable produces an opaque response independent of operation existence, state, bindings, or receipt content.
- That response reveals no protected data and grants no protected command effect; internal recovery bookkeeping is separate.
- Existing committed outcomes remain intact but undisclosed; processing metadata is exposed only after current authorization succeeds.
- A malformed envelope that cannot bind actor/operation/command is rejected fail-closed as **not an accepted operation**.
- Such rejection creates no implied reservation, terminal operation outcome, or accepted mutation.
- NEW admission requires authoritative proof that the authenticated actor/operation has no prior reservation and no prior effect.
- A missing lookup alone proves neither fact; ambiguous history returns authorized UNKNOWN, or the opaque authority response.
- NEW→reserved indivisibly persists original actor/operation, command, canonicalization version, full binding, and digest.
- Reservation precedes command validation that can produce terminal APPLIED, CONFLICT, or INVALID.
- Reserved intent→fenced processing→uncertain commit→authoritative proof/recovery uses one original operation identity.
- A fence excludes independent workers/effects for that intent; its implementation is an unresolved architecture obligation.
- Exact concurrent arrivals join/resume that intent; changed arrivals are rejected only when mismatch is proved.
- Concurrent P/Q cannot replace the winner’s binding, create independent workers, or each mutate under one actor/operation.
- Validation checks current authority, original expected revisions, source bindings, evidence predicates, and applicable money bounds.
- Validation CONFLICT/INVALID is durably immutable; terminal validation failure is not a resumable no-effect operation.
- APPLIED is established only with authoritative commit proof and immutable committed outcome.
- Uncertain commit returns UNKNOWN; neither absence of response nor absence of a record establishes absence of effects.
- Recovery must recover original identity/binding from authoritative evidence, never reconstruct reservation from retry payload.
- PROOF_COMMITTED includes original actor, operation, command, canonicalization version, full binding, digest, and committed outcome.
- PROOF_NOT_COMMITTED includes that original identity/binding and authoritative absence of committed effects; it need not include an outcome.
- Resumption additionally requires positive authoritative proof that **no terminal command outcome exists**.
- Missing or unavailable outcome records do not prove terminal absence; effect absence and terminal absence are independent.
- Permitted recovery resumes the same fenced original intent, rechecks current authority and ORIGINAL expected revisions, and persists its result.
- Stale/invalid originals become terminal CONFLICT/INVALID; corrected payloads cannot replace them under the same operation ID.
- Server-owned recovery must make progress under restored authority, evidence, comparison, and commit prerequisites; no client blind-new-ID recovery.
- Mutation retry separates payload-comparison response from original immutable outcome; status query separately retrieves proven outcome.
- Recovered changed Q against original P returns OPERATION_REUSE only after proved comparison, never APPLIED for Q.
- If original comparison is impossible, mutation retry remains nonterminal UNKNOWN even when P’s status is separately proven.

## 8. State, proof, and result matrices
| Entry/state | Required fact or event | Authorized response / transition |
|---|---|---|
| Unbound malformed envelope | Binding cannot be formed | Request rejection; no accepted operation |
| NEW | Positive no-reservation/no-effect admission proof | Indivisible original reservation, then validation |
| Presence ambiguous | History not established | UNKNOWN; no admission or effect |
| Reserved/processing | Same binding established, safe fence | Join or resume original work only |
| Uncertain commit | Neither decisive effect proof | UNKNOWN; recover, no blind replay |
| Terminal original | Immutable outcome recovered | Return original outcome for exact retry/status query |
| Changed retry | Original comparison proves mismatch | INVALID OPERATION_REUSE; original outcome unchanged |
| Comparison unavailable | Original binding/version cannot be compared | Mutation UNKNOWN; status independently queryable |
| Authority denied/unavailable | Any internal state | Opaque authority response; no protected disclosure/effect |

| Original binding | Effects proof | Terminal existence | Recovery behavior |
|---|---|---|---|
| Complete | COMMITTED | EXISTS, committed outcome recovered | Retrieve APPLIED; never resume effects |
| Complete | COMMITTED | UNKNOWN or outcome unrecoverable | UNKNOWN; no resume or fabricated outcome |
| Complete | NOT_COMMITTED | EXISTS, validation outcome recovered | Retrieve CONFLICT/INVALID; never resume |
| Complete | NOT_COMMITTED | EXISTS, outcome unrecoverable | UNKNOWN; no validation or effects |
| Complete | NOT_COMMITTED | ABSENT authoritatively proved | Resume original fenced intent under current authority/revisions |
| Complete | NOT_COMMITTED | UNKNOWN | UNKNOWN; no validation, resumption, or effects |
| Complete | UNKNOWN | Any | UNKNOWN; no resumption |
| Missing/unrecoverable | Any | Any | UNKNOWN; no fabricated binding or rebinding |
| Complete | Contradictory proofs | Any | UNKNOWN; fail closed pending authoritative resolution |
- COMMITTED paired with proven terminal ABSENT is inconsistent: recover proof/outcome, never synthesize or resume.
- Query of a proven terminal outcome bypasses command comparison, not authorization or identity proof.
- Terminal outcome and effects proof are distinct stored facts; UNKNOWN is a nonterminal response, not replacement history.

## 9. Incompatibility and error matrix
| Condition | Response / error | Preservation |
|---|---|---|
| Original expected revision stale | Terminal CONFLICT / STALE_REVISION | Newer receipt and original binding preserved |
| Root C versus endpoints A/B; root A4 versus endpoint A5 | Terminal INVALID / ENDPOINT_BINDING | No ignored third receipt or endpoint write |
| Same receipt twice; wrong source pair/proposal/prior decision | Terminal INVALID / PAIR_BINDING | Exact-pair provenance unchanged |
| Unsupported negative/refund/netting; bounds or sum failure | Terminal INVALID / PURCHASE_RECONCILIATION | Original/draft/refund evidence retained |
| Required uncertainty; payer unknown; nonfinal bill | NEEDS_REVIEW, or INVALID if RECONCILED asserted | No defaults, paid inference, or attribution closure |
| Unsupported confident duplicate disposition | Terminal INVALID / DISPOSITION_EVIDENCE | Candidate may remain UNRESOLVED |
| Proved changed operation reuse | Retry INVALID / OPERATION_REUSE | Original terminal outcome remains unchanged |
| Canonicalizer/binding/proof unavailable | Nonterminal UNKNOWN / recoverable blocked reason | No rebinding, new worker, or false validation |
| Denied or unavailable authority | Uniform opaque authority failure | No existence/status/binding disclosure |

## 10. Synthetic command
```json
{"command":"ResolveDuplicateLink","actor":"synthetic:actor-1","operationId":"synthetic:op-7",
 "receiptId":"synthetic:A","expectedRevision":"A5","proposalId":"synthetic:proposal-2",
 "endpoints":[{"receiptId":"synthetic:A","expectedRevision":"A5","sourceId":"synthetic:issuer/item-A","sourceVersion":"v1"},
              {"receiptId":"synthetic:B","expectedRevision":"B3","sourceId":"synthetic:issuer/item-B","sourceVersion":"v1"}],
 "disposition":"UNRESOLVED","evidenceRefs":["synthetic:photo-region"],"reason":"Purchase identity not established"}
```
- Synthetic only; server supplies original canonicalization metadata/reservation, and verifies both endpoint authority/revisions.

## 11. R07 Given/When/Then design cases
- **R07-01 (A09):** Given ordered original pages/source versions, when a correction changes a normalized field, then a new immutable revision retains original coordinates, page order, lineage, extraction, and evidence.
- **R07-02 (A22):** Given two actors at revision A5, when both valid corrections race, then at most one applies and the other receives terminal STALE_REVISION CONFLICT; exact retry preserves that outcome.
- Given positive unused-key admission proof, when P arrives, then NEW→reserved stores its complete original binding before validation; given ambiguous history, the same arrival yields UNKNOWN without reservation.
- Given simultaneous P/Q on one actor/operation, when reservation arbitrates, then one original binding wins; exact arrivals join and proved different arrivals receive reuse INVALID without replacement.
- Given initial P is terminal STALE_REVISION CONFLICT, when corrected-revision Q reuses its ID, then proved reuse is INVALID and P’s CONFLICT remains retrievable.
- **R07-03 (A10/A14):** Given uncertain material field, mismatched total, pre-tip/nonfinal bill, or unknown payer, when review runs, then each independently blocks RECONCILED; balancing arithmetic closes none.
- **R07-04 (A11):** Given identical source version, revised lineage, distinct identical purchases, or ambiguous photo/import match, when duplicate review runs, then apply the respective authenticated predicate or UNRESOLVED, never automatic accounting merge.
- Given root C with A/B, or root A4 with endpoint A5, when proposing/resolving/reversing, then terminal ENDPOINT_BINDING INVALID occurs with no endpoint effect.
- Given a valid exact-pair reversal, when both authorities/revisions pass, then both update atomically and prior decision/source provenance remains; either endpoint failure leaves both unchanged.
- **R07-05 (A18/A19):** Given malicious receipt instructions, when extracted/displayed, then they remain data; unauthorized or authority-unavailable reads/mutations/queries return opaque responses independent of hidden operation state.
- **R07-06 (A22):** Given interruption before response, when an authorized client queries status, then a proven immutable outcome is retrieved or UNKNOWN is returned; no invented confirmation or blind replay follows.
- Given missing local record and recovered committed P with full original binding/outcome, when changed Q retries, then proved mismatch yields reuse INVALID, never APPLIED for Q; missing binding yields UNKNOWN.
- Given established terminal status and unavailable original canonicalizer, when status is queried, then retrieve it without payload comparison; when mutation retries, then comparison-blocked UNKNOWN leaves that status unchanged.
- Given prevalidation reservation interruption, full original binding, no-effects proof, and positive terminal-absence proof, when recovery proceeds, then resume original fenced intent using current authority and original expected revisions.
- Given instead an existing validation failure, when recovery obtains it, then retrieve it without resumption; if existence is known but outcome unavailable, remain UNKNOWN without effects.
- Given persisted INVALID/no effects but unavailable terminal-existence evidence, when recovery runs, then UNKNOWN forbids validation/resumption; missing outcome is not terminal absence.
- **R07-07 (A10/A14/A15):** Given supported final integer total and attributed contributions plus explicit unpaid, when bounded equality holds, then arithmetic is eligible, not accepted debt; unknown currency/amount, zero defaults, overpayment, negative unpaid, mismatch, or unsupported refunds prevent reconciliation.

## 12. Coverage, independent review, and blockers
| Coverage inventory | Required independent check |
|---|---|
| Originals, immutable revisions, uploader/owner/payer separation | R07-01; data matrix; custody against full source documents |
| Concurrency, admission, reuse, recovery, terminal persistence | R07-02/06; every state/proof row; all recovered-binding counterexamples |
| Material eligibility, finality, payer and bounded money | R07-03/07; unknown/zero/negative/refund cases |
| Duplicate predicates, exact pair, reversal atomicity | R07-04; both endpoints/source versions/revisions/authority and binding |
| Injection, access, revocation and opaque failures | R07-05; current authorization for reads, retries, queries, and recovery |
| Canonicalizer/query separation and immutable outcomes | Paired R07-06 cases; retry errors never overwrite original status |
| Traceability and publication custody | Full GOAL_PROMPT/TRANSACTION_MODEL/ACCEPTANCE/#9 comparison; baseline/path and ≤399 gate |
- Reviewer must independently check all fourteen corrected seams, all seven R07 cases, matrices, examples, and original TASK obligations; no overflow deferral.
- SPEC-00/#2 authority, qualified ingestion, roles, hosting, retention/deletion, and key recovery block implementation and admission of real uploads.
- Parent #9 still owes upload safety, OCR, license review, phone visual contract, and whole SPEC-07 integration.
- Later implementation requires approved architecture, exact allowed runtime files, executable gates, negative cases, and whole-product seams; none are invented here.
- Financial/security review remains mandatory; this paper grants no execution, financial, security, architecture, or product approval.
- #50 remains OPEN until exact artifact custody, independent review, traceability links, and publication evidence are verified; #9 remains OPEN.
- No enrollment, private deployment, purchases, paid inference, license adoption, outreach, or hidden “done pending” closure is claimed.

**UNREVIEWED/UNEXECUTED**