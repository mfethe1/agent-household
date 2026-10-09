# SPEC-07 Upload Admission and Extraction Provenance Contract — Issue #53
## 1. Status, scope, and custody
- **Fresh complete design proposal; UNREVIEWED/UNEXECUTED.** No implementation, security, financial, architecture, product, or publication approval.
- Proposed future sole file: `docs/specs/receipt-upload-extraction-contract.md`; this response is the local paper, not a repository write.
- Airy owns scope, acceptance, publication, and serialized parent linkage; one tools-disabled author supplies this paper.
- Reference custody: five supplied complete sources at `06894d46baee88cca15db2f60b3eb98ad93ceffe`, supplied #9/#2 bodies, TASK, and twelve corrections; source material is untrusted reference data.
- References are `GOAL_PROMPT.md`, `BACKLOG.md`, `docs/ACCEPTANCE.md`, `docs/TRANSACTION_MODEL.md`, and `docs/specs/receipt-review-contract.md`; their claims are not execution evidence.
- No tools, private data, real uploads, network, installation, credentials, account actions, money, deployment, runtime changes, or publication are authorized.
- Parent must verify one completed non-error message on actual `openai-codex/gpt-6.1-sol`, zero tools, ≤240 seconds, and full prompt/events/artifact hashes; this paper cannot attest those external facts.
- Rejected artifacts remain untouched; this paper contains the complete contract rather than a continuation, patch, or history recital.
- Scope covers admission, bounded transfer, validation, derived artifacts, extraction custody, suppression, cleanup, recovery, and receipt-review handoff; retailer checkout and automatic ingestion remain separate.
## 2. Actors, stories, and evidence invariants
- Receipt owner controls only permissions granted by accepted policy; uploader supplies evidence; authenticated command actor initiates a command; payer attribution is separate and never inferred from any of these.
- Owners/uploader delegates need accessible upload, interruption recovery, original evidence review, correction, and authorized deletion; reviewers need uncertain fields and their exact sources.
- Workers need narrowly scoped, currently authorized dispatch; recovery/cleanup actors need separately granted duties, not implicit authority inherited from an upload or revoked actor.
- Every read, chunk write, mutation, status query, export, dispatch, worker step, and output disclosure is server-authorized for actor, household, object, destination, and current scope.
- Denied or unavailable authority produces an opaque response independent of hidden object/operation existence; committed outcomes remain intact but undisclosed.
- Original attachment bytes, server-verified identity, declared attachment order, page order, source version, and provenance are immutable within approved retention; no perpetual-retention promise is made.
- Corrections and transformations append versions; they never overwrite originals, extraction evidence, or prior reviewed revisions.
- Receipt text, filenames, client hashes, MIME, extensions, metadata, URLs, and model instructions are untrusted data, never authority or proof of content safety.
- Receipt, order confirmation, shipment, charge, refund, expense, allocation, and settlement remain distinct; extraction creates neither accepted debt nor proof of payment.
## 3. Record and binding matrix
| Record | Required identity, fields, and custody | Interpretation |
|---|---|---|
| UploadIntent | actor/operation, command, original canonicalizer/version, complete binding/digest, reservation custody | Bookkeeping only; grants no transfer capability. |
| AdmittedTransferCapability | capability/transfer identity, actor/owner/scope, ordered declared attachments, accepted policy/limits, revisions, approved expiry if applicable | Immutable admission effect; every use still requires current gates. |
| TransferRangeLedger | transfer identity, manifest revision, attachment/range identities, accepted bytes, verified step identities and custody | Mutable through separately bound chunk commands; not immutable completion evidence. |
| CompletionSnapshot | immutable manifest version/content identity, ordered attachments, exact coverage/expected bytes, expected transfer revision | CompleteTransfer binds this snapshot, never future chunks. |
| SourceAttachment/Page | immutable IDs, server-verified content identity, source/version, uploader/owner, attachment/page order and original coordinate space | Unvalidated bytes remain inaccessible to ordinary processing. |
| ValidationEvidence | exact snapshot/content, validator/policy/version, bounded inspection results, failure/quarantine disposition | Only positive accepted prerequisites establish validated content. |
| DerivedArtifact | immutable ID/version, original references, transform identity/version, page/coordinate mapping, verification results | Unverified mapping is explicit failure, not invented provenance. |
| Extraction | immutable extraction/version, originals/derivatives, engine/model/version/digest where available, destination/consent, fields/confidence/absence/uncertainty | Unknown metadata explicit; no unsupported reproducibility claim. |
| SuppressionBarrier | immutable barrier reference, affected scope/actions, establishing command, policy/revision and responsibility references | Reference identity is distinct from current applicability/compatibility. |
| ContinuationResponsibility | separate operation/binding, barrier references, exact disposition/step set, credited custody, current fence, successor/transfer evidence | Cleanup or maintenance cannot reopen its parent command. |
| OperationEvidence/Outcome | original binding, step ledger, distinct effect/terminal/disposition proofs, immutable result and permitted details | UNKNOWN is a response, never replacement terminal history. |
- Every mutation binding **B** includes authenticated actor/namespace, operation ID, command, targets/owner/scope, original expected revisions, all referenced versions, semantic payload, policy/consent/destination, disposition and reason.
- Add command-specific capability, manifest, range, source/order, barrier, target-operation, cleanup-step and responsibility identities wherever applicable; semantically relevant fields cannot be omitted.
- Persist B with original canonicalization version and digest before validation; recover B authoritatively, never reconstruct it from retry payload; digest alone is insufficient binding custody.
- Exact retry compares using that original canonicalizer; unavailable comparison gives mutation UNKNOWN, while an authorized payloadless status query independently retrieves proven status without canonicalization.
## 4. Independent proofs and common result matrix
- **R0** proves no original reservation in the actor/operation namespace; missing lookup is not R0.
- **F0(c)** positively proves absence of command c’s named successful final domain effect; **F1(c)** proves that exact effect committed, independently of terminal existence or recoverable outcome.
- **T0(c)** positively proves no terminal outcome exists; **T1(c)** proves terminal existence; **O(c)** recovers the original immutable outcome. T1 without O is not a usable result.
- **L(c)** is the authoritative partial-step ledger: complete committed-step custody, original binding/step identities, and exact remaining-effect calculation; PARTIAL alone proves neither F0 nor T0.
- **D0/D1(c)** independently prove absence/commit of the exact failure disposition; recording a terminal failure must not be confused with successful final-effect publication.
- **W(c)** proves current exclusive fence and active-execution identity; reservation, W, and exact comparison never establish F0 or T0.
- **S(c)** proves command/scope-specific current suppression applicability and compatibility; absence, applicable barrier, conflict, and uncertainty are distinct, authoritative results.
- **PROOF_COMMITTED** means complete B + F1 + T1 + O for the original successful operation; **PROOF_NOT_COMMITTED** means complete B + F0 and requires no nonexistent outcome.
- Complete success effects with absent/unrecoverable outcome yield UNKNOWN/no repetition; inconsistent proof combinations fail closed for authoritative reconciliation.
| B / successful effect / terminal proof | Authorized result and permitted action |
|---|---|
| Complete / F1 / T1+O | Return immutable APPLIED; never restart or resume. |
| Complete / F1 / terminal unknown, absent, or O unavailable | UNKNOWN; reconcile inconsistency or missing outcome, never repeat effects. |
| Complete / F0 / T1+O with consistent disposition proof | Return original CONFLICT/INVALID/FAILED/CANCELED; never resume. |
| Complete / F0 / T1 without O | UNKNOWN; no validation, continuation, or fabricated failure. |
| Complete / F0 / T0 / complete L and applicable current gate+W | Only original evidenced remaining work may progress; no committed-step replay. |
| Complete / unknown F0 or unknown terminal existence | UNKNOWN; no validation, successful work, failure terminalization, or restart. |
| Missing B, incomplete L, contradictory evidence, or uncertain disposition commit | UNKNOWN; preserve suppression, resolve custody, no rebinding or replay. |
- Each failure result is immutable only when its exact disposition and outcome commit atomically under G-FAIL; uncertain disposition/outcome commit is UNKNOWN, not permission to repeat it.
## 5. Gate matrix — applies to every command, state, race, and case
| Gate | Required proofs and current authority | Limits |
|---|---|---|
| G-NEW | authenticated bindable envelope, R0, command-specific F0/T0, current admission authority/consent/policy/revisions/S, exclusive reservation arbitration | Persist B before validation; unknown history denies admission with UNKNOWN. |
| G-ORD | B, F0/T0, L, W, current ordinary authority, scoped consent, accepted processing policy/destination/limits, original revision compatibility and compatible nonsuppressed S | Admission publication, transfer, validation, extraction and publication each use their own named F0. |
| G-MAINT | B, F0/T0, L, W, current narrow command-specific suppression-maintenance authority/policy/scope, original compatible revisions, positively known S | Before barrier existence, lawful barrier-establishment prerequisites must independently hold; no assumed barrier. |
| G-CLEAN | B, F0/T0, L, W, applicable durable barrier plus current cleanup authority/policy/scope and original revision compatibility | Only minimal authorized storage access for exact disposition; never weaken suppression. |
| G-FAIL | B/canonicalizer custody, F0/T0, L, W, authoritative failure reason and current narrow authority to record that exact disposition, D0 | Does **not** require the failed revision, suppression, consent, or processing-policy prerequisite. |
- G-FAIL may record stale CONFLICT, invalid INVALID, resource FAILED or suppression CANCELED; it grants no successful remaining work, ordinary read, extraction, disclosure, restoration, or publication.
- Revoked processing authority itself grants no failure-terminalization authority; if narrow authority or any required proof is absent, remain opaque/UNKNOWN rather than inventing a result.
- G-MAINT/G-CLEAN are not ordinary-use exceptions: no decoding for ordinary extraction, external model transfer, restoration of visibility, or publishing partial fields.
- NEW, processing, concurrency, retry, interruption and recovery rows inherit these gates explicitly; terminal retrieval requires current read authority and proven identity/O, not F0/T0.
- Joining an exact proven active execution requires B/comparison, F0/T0, L, W and its current applicable gate; joining creates no extra worker or effects. Otherwise UNKNOWN or immutable retrieval.
- Restarting interrupted work requires fresh independent F0/T0/L/W and its current gate; it resumes only original remaining work, not committed chunks, steps, or outputs.
## 6. Command, successful final effect, and atomic terminalization matrix
| Command | Additional immutable binding | Successful final domain effect and terminal point |
|---|---|---|
| AdmitUpload | ordered declared manifest, transfer identity, owner/scope, approved policy/limits/revisions/expiry | Capability publication + immutable APPLIED atomically; intent reservation is not F1. |
| PutChunk | exact capability, transfer/manifest revision, attachment/range, expected bytes/content identity | Accepted range/bytes and new manifest revision + APPLIED atomically; duplicate steps credited by L. |
| CompleteTransfer | exact snapshot/version/content identity/order/coverage/expected bytes and expected transfer revision | Immutable completed-transfer evidence + APPLIED atomically; no mutable-ledger inference. |
| AbandonTransfer | exact transfer/capability, scope, expected revision and approved disposition | Suppression/disposition plus separately bound cleanup responsibility + APPLIED atomically. |
| ValidateContent | completed snapshot, original identities/order, accepted validation policy/limits | Immutable validated-original evidence + APPLIED atomically; unsafe content never qualifies. |
| ExtractReceipt | validated inputs/mappings, processing identity, accepted output policy, consent/destination, expected receipt revision | Safe authorized immutable extraction/draft publication + APPLIED atomically; never reviewed accounting. |
| CancelOperation | exact target B/operation, suppression scope, expected revisions, approved cleanup disposition | Winning barrier + target CANCELED/O + cancellation APPLIED/O + separate cleanup responsibility atomically. |
| RequestDeletion | exact scope, policy, barrier compatibility, revisions, responsibility/transfer disposition | Durable applicable barrier and complete responsibility establishment/transfer + APPLIED/O atomically; not cleanup-complete. |
| CleanupContinuation | separate B, immutable barrier refs, exact disposition/steps, credited custody | Exact approved cleanup disposition completed + APPLIED/O atomically; completion claim requires policy proofs. |
| MaintainBarrier/TransferResponsibility | separate approved B, scope, barriers, predecessor/successor custody and original revisions | Exact barrier maintenance or authoritative responsibility transfer + APPLIED/O atomically. |
| QueryOperation | authenticated actor/operation reference only | Authorized proven original status; no mutation or canonicalizer binding. |
- Every successful row requires its applicable §5 gate; every unsuccessful terminal row uses G-FAIL with its separate atomic disposition/outcome transaction. Transaction realizability is an architecture blocker, not a selected implementation.
## 7. Upload, validation, and extraction domain transitions/results
| Domain entry/event | Exact result, disposition, and next domain state | Retry/recovery rule |
|---|---|---|
| Unbindable envelope | Request rejection, no accepted operation/capability/outcome | Correct request may be admitted only via G-NEW; no implied intent. |
| Intent reserved; before capability publication | RESERVED, no chunk authority; interruption nonterminal | Resume AdmitUpload only B/F0(capability)/T0/L/W/G-ORD; F1 without O → UNKNOWN/no grant repetition. |
| Admission prerequisite fails after reservation | G-FAIL immutable CONFLICT/INVALID/FAILED with exact no-capability disposition | Exact retry/status returns original; cannot grant capability through failure path. |
| Capability APPLIED | ADMITTED; transfer may begin only with exact capability and current G-ORD | Admission retry returns APPLIED; capability is not standing authorization. |
| Accepted chunks / interrupted transfer | TRANSFERRING/INTERRUPTED with bounded range ledger, not complete evidence | Separate chunk operations may fill ranges under capability/current G-ORD/version checks; interrupted chunk resumes only its original remainder. |
| Stream bytes/limits/resource violation | G-FAIL immutable INVALID/LIMIT or FAILED/RESOURCE with bound range disposition | Original retry returns failure; abandonment/cleanup only if separately approved and bound, never assumed. |
| Completion snapshot has proved missing ranges | G-FAIL immutable INVALID/INCOMPLETE_MANIFEST; snapshot rejected | Old retry stays INVALID; underlying transfer remains fillable unless explicit approved disposition abandons it. |
| Completion proved truncation/content mismatch | G-FAIL immutable INVALID/TRUNCATED_OR_MISMATCH and approved quarantine/disposition | Old retry unchanged; no silent substitution, repair, validation, or payload alteration. |
| Completion coverage or commit proof unknown | UNKNOWN; no invented rejection/completion | Recover original snapshot proofs; no blind replay or waiting for new chunks to change B. |
| Complete snapshot computation interrupted with F0/T0 | Same snapshot remains pending | B/L/W/G-ORD allows original remaining computation only; later manifest revision requires deliberate distinct command. |
| CompleteTransfer APPLIED | COMPLETED immutable content/order/coverage evidence | Exact retry/status returns APPLIED; mutable range ledger alone never proves this effect. |
| Abandonment wins under approved gates | ABANDONED/suppressed plus separately bound cleanup; immutable APPLIED | No further ordinary chunks; cleanup uses G-CLEAN and never reopens abandonment. |
| Validation supported and all prerequisites proved | VALIDATED, immutable validation evidence | APPLIED immutable; later extraction separately bound/currently authorized. |
| Malformed/unsupported/encrypted/polyglot/active/bomb/oversize content | G-FAIL immutable INVALID/UNSAFE_OR_UNSUPPORTED plus exact approved rejection/quarantine | Originals never become validated; exact retry returns failure, no unsafe decoder/model call. |
| Validation resource exhaustion | G-FAIL immutable FAILED/RESOURCE and exact atomic failure disposition | No impossible requirement to prove absence of that disposition after committing it; failure never resumes. |
| Validation interrupted / safety or commit proof unknown | Nonterminal interrupted only with F0/T0/L; otherwise UNKNOWN | Original bounded remaining validation only under G-ORD; no inference of safety from interruption. |
| Extraction computed fields not published | Unpublished partial computation in L, not extraction success | F0(publication)/T0/L/W/G-ORD permits only remaining authorized work; no disclosure of staged fields. |
| Approved safe partial publication | APPLIED with explicit PARTIAL_SAFE outcome, uncertainty and NEEDS_REVIEW | Policy/partial mode and prior consent must be bound before admission; immutable result, no resumed terminal extraction. |
| No approved partial policy / unsafe partial | Admission blocked; or G-FAIL immutable INVALID/POLICY or FAILED with exact unpublished-field disposition | No invented default partial output; originals/uncertainty retained only within accepted retention policy. |
| Extraction bounded resource failure | G-FAIL immutable FAILED/RESOURCE; no successful publication | Exact retry returns failure; distinct new attempt needs lawful deliberate admission, not blind recovery. |
| Extraction full publication committed; outcome missing | F1(publication), UNKNOWN until O recovered | Never repeat publication, create a replacement draft, or infer no effect from missing response. |
| Extraction APPLIED | EXTRACTED/NEEDS_REVIEW with immutable evidence-linked draft | Exact retry returns original; review eligibility/accounting handled only by existing review contract. |
## 8. Retry, suppression, cancellation, deletion, and responsibility races
| Condition/race | Required decision and immutable/pending result |
|---|---|
| Exact concurrent arrival | Join only §5’s proven active execution; otherwise original remaining work under full restart proofs, immutable retrieval, or UNKNOWN. |
| Proven changed reuse | Retry INVALID/OPERATION_REUSE, not replacement terminal outcome; original B/O remain intact. Comparison unavailable → mutation UNKNOWN. |
| Missing response/record, uncertain final or disposition commit | UNKNOWN/no additional effects; authoritative recovery of B/F/T/D/L/O is required; no blind new-ID replay. |
| Original prerequisite stale/revoked/suppressed | Successful work forbidden; G-FAIL may terminalize exact CONFLICT/INVALID/CANCELED, otherwise opaque/UNKNOWN; no silent rebinding. |
| Cancel intent only | PENDING, not proven canceled or APPLIED; G-MAINT may progress only under its lawful pre-barrier prerequisites and known S. |
| Cancellation winner | Current cancellation authority plus own B/F0/T0/L/W/G-MAINT and independent target B/L/fence/positive target F0/T0 permit the §6 atomic winner transaction. |
| Target completed winner | Recover target immutable outcome; cancellation uses its **own** G-FAIL and authoritative losing-race evidence for immutable CONFLICT/TARGET_COMPLETED; target F0/T0 are not required. |
| Cancellation crash before winner transaction | No APPLIED claim; only positively proved original remaining work may progress under applicable gates; otherwise UNKNOWN. |
| Cancellation crash after winner transaction | Retrieve both immutable outcomes; separate cleanup continues via G-CLEAN; target/cancel never reopen or publish staged fields. |
| Unknown target/cancel effect, terminal existence, or outcome | UNKNOWN/no replay; preserve any lawful suppression. Unapproved atomic boundary blocks implementability, not permission for split winner commits. |
| Deletion with no barrier | G-MAINT plus current deletion authority/accepted policy and known compatible scope establishes barrier/responsibility atomically; pending intent alone is not suppression. |
| Deletion with compatible cancellation/deletion barrier | May preserve or strengthen barrier under current policy/authority; APPLIED requires exact responsibility establishment/transfer, never a false fresh-barrier or cleanup-complete claim. |
| Conflicting scope, stale revisions, uncertain barrier | G-FAIL immutable CONFLICT only with authoritative reason and own proofs; uncertainty → UNKNOWN; no weakening, ordinary access, or invented compatibility. |
| Deletion barrier committed/outcome unavailable | UNKNOWN/no repetition; recover O and responsibility; barrier remains. APPLIED cannot precede barrier/responsibility and orphan later work. |
| Deletion APPLIED; cleanup unavailable/partial | Original APPLIED immutable; separate cleanup pending/UNKNOWN according to its own proofs, with barrier preserved and explicit credited steps/remaining work. |
| Cleanup disposition complete | Separate cleanup APPLIED only with full accepted original/derived/cache/model-destination/backup disposition proofs required by policy; otherwise pending/UNKNOWN, never “deletion complete.” |
- Exact deletion retry retrieves original outcome; a distinct deliberate deletion command is separately admitted and bound, may strengthen compatible suppression, and cannot duplicate prior responsibilities or claim prior steps as fresh work.
- D1/B1/C1 → D2/B2: current applicability is proved independently of immutable references; if C1 original revisions remain compatible, retain its exact B/responsibility without adopting D2 revisions.
- If C1 is stale, G-FAIL may atomically terminalize fenced C1 CONFLICT only with positive F0/T0, complete L, narrow current disposition authority and stale evidence; its B is never rewritten.
- D2’s effect, or a separate approved transfer command, must atomically establish separately bound C2 and authoritative responsibility transfer, crediting C1 committed steps and computing exact remaining work without duplicate ownership.
- Unknown C1 final effect/terminal/outcome or incomplete step custody prevents unsafe transfer/replay: D2 stays pending/UNKNOWN unless its approved atomic effect can establish complete nonduplicating responsibility; suppression remains.
- Abandoned/stale responsibility recovery identifies the original custodian, ledger and fence; successor creation requires approved transfer proofs. C2 progresses only under its own B/G-CLEAN, never reopens terminal D1/D2/C1.
## 9. Safety, privacy, disclosure, and review compatibility
- Accepted SPEC-00/security policy must select supported types, preflight/scanning/quarantine strategy, safe parsers, isolation, storage and destinations; unknown selections block admission and real uploads.
- Explicit numeric byte/chunk/attachment/page/pixel/decompression/memory/CPU/time/concurrency/network/retry/output limits are implementation blockers until selected; enforce bounded resources at transfer, inspection, decode, transform, model, publication and recovery seams.
- Unsafe/unverified content cannot become readable evidence accidentally; no filename-derived paths, active rendering, executable receipt content, or external URL fetch from documents.
- Model processing requires prior current scoped consent and disclosed destinations/handling; local-upload consent never authorizes third-party transfer. Injection-safe display and model outputs cannot authorize tools or actions.
- Sensitive storage/backups require approved encryption/key recovery; logs, errors, public evidence and operation details contain no private bytes/secrets. Restore checks current barriers before any ordinary access/output.
- Review handoff preserves versioned extraction fields, originals/order/mappings, uncertainty, finality and evidence; integer minor-unit bounds, explicit currency/payers/unpaid and exact conservation remain the review contract’s obligations.
- Missing/low-confidence fields, nonfinal bills, inconsistent totals and unknown payer remain NEEDS_REVIEW; no zero defaults, invented payers, accepted accounting, automatic merge or silently rewritten settled history.
- Existing review corrections/reconciliation/duplicate commands retain full bindings, exact-pair/source-version predicates and atomic endpoint effects; these upload gates strengthen, never relax, their independent proof/recovery requirements.
## 10. Given/When/Then design cases and exact future verification seams
| Case / mapping | Given / When / Then and required verification seam |
|---|---|
| U07-01 / A09 | Given distinct owner/uploader/actor/payer and ordered originals, when transforms/corrections occur, then immutable identities/order and verified original-coordinate mappings survive; verify byte identity, page ordering, mapping versions and failure visibility. |
| U07-02 / A19 | Given spoofed MIME/extensions, polyglots, active/encrypted/truncated files or bombs, when admission/validation evaluates prerequisites, then unsafe/unsupported results are immutable or uncertainty stays blocked; instrument zero unsafe decoder/model invocations. |
| U07-03 / A19,A22 | Given bounded streaming and missing ranges 0–99 + 200–299, when limits/interruption/completion occur, then resource failures terminalize lawfully, snapshot completion returns immutable INCOMPLETE_MANIFEST; after chunk 100–199, old retry stays INVALID and only distinct newly bound completion may succeed. |
| U07-04 / A10 | Given partial/low-confidence OCR, unknown model metadata, nonfinal bill, inconsistent total or resource exhaustion, when extraction finishes/fails, then explicit uncertainty/NEEDS_REVIEW or immutable FAILED remains; verify approved safe-partial mode versus unpublished fields and no accepted accounting. |
| U07-05 / A18,A19 | Given cross-household attachment/status/extraction, revocation, malicious instructions/URLs, display injection or missing destination consent, when reads/dispatch/publication occur, then opaque denial or lawful failure/UNKNOWN reveals nothing and authorizes no action; verify all interface/worker seams. |
| U07-06 / A20,A22 | Given reservation, capability, completion and extraction crash cuts, when exact/changed/concurrent retries/status/recovery occur, then independent proofs select original outcome/remaining work/UNKNOWN without orphan draft or replay; test reservation-only no chunk authority, missing-range old/new completion and isolated restore hash/order/mapping custody. |
| U07-07 / A21 | Given processing races, cleanup unavailable, delayed outputs, backup restore and D1/B1/C1→D2/B2, when cancellation/deletion/revocation wins or loses, then atomic immutable outcomes, preserved barriers and nonduplicating successor custody hold; test APPLIED deletion→cleanup, cancellation→new deletion, stale C1 G-FAIL and unknown transfer blockers. |
| U07-08 / A09,A10,A22 | Given uncertain versioned draft and legitimate identical purchases, when review handoff and accessible phone/keyboard/screen-reader upload/progress/error/status recovery occur, then evidence/uncertainty persist and purchases are not auto-merged; verify shared backend contract, not a selected visual design. |
- These are future synthetic adversarial scenarios, **not passing runtime tests**; executable fixtures must assert each command effect, disposition, terminal retry/status, proof cut, fence, disclosure and policy blocker.
## 11. Dependencies, independent review, and closure
- Dependency DAG: accepted #2/P0-02/03/04 authority/financial/architecture/security policies → qualified upload/processing/recovery implementation → E1 review handoff → E2/E3; retailer access blockers remain independent.
- Parent spec/security reviewer owns unresolved roles/sharing/hosting/storage/retention/deletion/backup-expiry/tombstones/keys/worker/source/consent/destination/type/limit policies; named owners still require assignment where backlog says unassigned.
- Parent #9 separately owns phone visual contract and Receipt Wrangler license/fit review; no adoption, license clearance, third-party capability, financial approval or closure is implied.
- Fresh independent full-source review must reconcile every B/F/T/D/L/gate, command/state/result/race row, all eight cases, both predecessor contracts and twelve corrections; parent resolves findings against exact artifact custody.
- Only accepted exact bytes may be staged under separate publication lease: strict full-repository gates, ≤399 canonical additions+deletions, independent publication review, fresh merged checks, byte-identical GitHub blob and serialized #9 links.
- Never drop coverage to fit publication; implementation children require approved dependencies, exact allowed files, executable tests, cleanup and whole-product seams. This paper admits none.
- Issue #53 remains unaccepted until its gates pass; #9, #2 and the overall product goal remain **OPEN**.