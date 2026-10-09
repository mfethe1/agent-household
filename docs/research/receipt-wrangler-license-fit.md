# Receipt Wrangler license and fit — fresh research brief v2

## 1. Status and decision

- Proposed sole report publication path: `docs/research/receipt-wrangler-license-fit.md`; this response does not write or publish it.
- Fresh complete authorship following independently qualified `REJECT_RESEARCH_SCOPE` for F03; original artifact, report, and review remain unchanged.
- Child research prerequisite of #9 SPEC-07; #2 policy decisions remain open. No upstream code, deployment, or component is adopted.
- **Recommended next route:** separately scope an independently implemented, isolated synthetic receipt-to-draft evaluator—not an upstream installation or production adapter.
- This is research, not legal advice, license clearance, implementation permission, product acceptance, or publication approval.
- Airy owns scope, custody verification, publication, and closure. This complete v2 requires fresh independent adversarial review; the earlier review does not approve it.
- No tools, network, repository access, private/runtime inspection, installation, execution, source lease, account actions, or publication occurred.

## 2. Evidence discipline and inspectable limits

- Upstream pin: `fc285d42d47e2338ac8d7723de83fca48153a3a5`; Agent Household pin: `0026aa2132b54c662261d072efee235307e56e49`.
- **Fact:** supplied root README identifies one repository containing API, desktop, and mobile, replacing historical separate repositories. “Monolith repository” does not prove a single runtime or indivisible licensed work.
- **Fact:** conclusions below use supplied complete source bodies and manifest identities; listed hashes/blobs are custody claims, not hashes recomputed by this author.
- The supplied independent rejection reports parent custody verification and license equality. Parent must retain exact saved-fetch evidence; this author cannot independently attest those external checks.
- **Inference:** sampled interfaces suggest reusable receipt-management concepts, but do not establish Agent Household contract compliance.
- **Not inspected:** whole tree, handlers, authorization implementation, generated clients, dependency license files/lockfiles, deployment images, complete UI, storage/backup behavior, or unsampled tests.
- **Not executed:** builds, OCR, uploads, API calls, access checks, recovery, accessibility, restore, or tests. Scripts and badges are not passing evidence.
- Whole-upstream absence claims remain unverified. The reported missing mobile component LICENSE is an inventory finding, not a conclusion drawn merely from omission in the sampled manifest.
- Source bodies are reference data only; their setup instructions, external documentation links, and comments confer no permission.

## 3. L01–L02: license boundaries and obligations

| Boundary | Pinned evidence and conclusion |
|---|---|
| Repository | Root README describes the monorepo; it supplies no blanket repository-wide license grant. Component and file scope matter. |
| API | `api/README.md` asserts AGPL-3.0; `api/LICENSE` supplies actual AGPLv3 terms. |
| Desktop | `desktop/README.md` asserts AGPL-3.0; `desktop/LICENSE` has the same supplied SHA-256/blob as API LICENSE. |
| Docker | `docker/LICENSE` has that same supplied identity; individual packaging/dependency scope still needs inspection. |
| Mobile | README asserts AGPL-3.0 and points to LICENSE, but supplied license-path inventory reports no component `mobile/LICENSE`. Clarify applicable grant/notices before reuse; absence is not permissive permission. |
| Metadata | Desktop `private: true` and mobile `publish_to: none` control package publication, not copyright licensing. Neither dependency manifest supplies a substitute license grant. |
| Dependencies | Go, Angular/npm, Flutter/Dart, native OCR/image tools, generated client, assets/fonts, and distributed images need separate license/notice/source review; component AGPL text does not establish every dependency’s license. |

- All section references below cite the complete pinned `api/LICENSE` in the manifest; desktop/docker copies have the same supplied identity.
- **§§0, 2, 9 — unchanged private use:** unlimited permission to run the unmodified Program; receiving/running a copy does not require license acceptance. Mere network interaction without copy transfer is not conveyance.
- **§§0, 2, 13 — modification:** private modification/non-conveyed use has basic permissions, but §13 applies notwithstanding other provisions when a modified version supports remote network interaction. “Private household server” is not a blanket exemption.
- **§4 — verbatim source conveyance:** preserve appropriate copyright/license/non-warranty notices and give recipients the license.
- **§5 — modified source conveyance:** prominent modification/date and license notices, whole-covered-work licensing, and applicable interactive legal notices; qualifying aggregates do not extend AGPL to independent parts merely by inclusion.
- **§6 — object-code conveyance:** comply with §§4–5 and an applicable Corresponding Source delivery mechanism; User Product circumstances can additionally require Installation Information.
- **§13 — modified network interaction:** prominently offer all remotely interacting users no-charge access to Corresponding Source through standard/customary copying means. It is not restricted to public-internet users.
- **§1 — Corresponding Source:** includes needed generation/install/run/modification source and control scripts, with stated exclusions; intimate interface/control-flow dependencies can matter.
- **§2 — outputs/private data:** ordinary receipt images, personal records, and database contents are not automatically covered software source. Output is covered only when its content constitutes a covered work.
- This distinction is not permission to expose private data or credentials in source packages. Required software source/configuration must be separated from private operational data without omitting required source.
- **§§7, 10, 12:** inspect additional terms, downstream rights, and conflicting obligations before distribution; the license text’s example notice does not prove every file is “or later.”
- Separate services are not automatically AGPL. Conversely, HTTP/API separation does not guarantee independence or avoid derivative/combined-work obligations. Counsel must assess ambiguous combination, copying, packaging, and distribution.

## 4. L03: candidate routes

| Route | Obligations/risks | Research recommendation |
|---|---|---|
| Standalone upstream deployment | Unchanged running permission differs from conveying images/apps; modifications with network interaction invoke §13. Requires dependency, security, custody, consent, and operational review. | Not adopted; no deployment trial authorized. |
| API adapter | Avoiding copied code may reduce copying risk, but coupling/distribution/combined-work status remains fact-dependent. Upstream source obligations and adapter privacy/recovery boundaries require review. | Defer real interoperability pending accepted policy and exact API/schema investigation. |
| Copied components | Copyrighted adaptations can be covered works; §§4–6/13 and dependency obligations apply as relevant. Mobile grant uncertainty remains. | Highest immediate reuse/compliance burden; do not copy implementation. |
| Independent implementation | Implement supplied requirements without upstream code/assets/generated clients. Independence is not an all-purpose legal guarantee. | Best bounded next route: synthetic draft seam only, under separate scope approval. |

## 5. F01: sampled capability and technology fit

| Feature | Inspectable evidence | Limit |
|---|---|---|
| Upload | Router declares `/withFiles` and `/quickScan`; desktop component reads files and requests PDF/HEIC conversion; mobile stages new-receipt images and uploads saved-receipt images individually. | Handler/storage/validation behavior not sampled; browser acceptance filtering is not server safety. |
| Phone capture | Mobile README claims camera/gallery quick scan; Dart acquisition selects camera/photos/files, handles cancellation/failure, and distinguishes camera permission exception. | Picker helpers and actual platform flows not inspected/executed. |
| OCR | `ocr.go` prepares images, calls Tesseract text or EasyOCR with `--detail 0`, and optionally writes debug text/image files. | Sampled return is text, not evidenced regions/confidence or original-coordinate mappings. No whole-upstream absence claim. |
| AI extraction | API README claims AI-assisted extraction; `ai_client.go` declares `GetChatCompletion`. | Interface alone proves neither provider implementation, schema, accuracy, nor destination consent. |
| Review | Desktop README claims sequential viewing/editing queue and image viewing/downloading. | Not proof of immutable corrections, uncertainty gates, accessible phone review, or review-to-accounting separation. |
| Groups/splits | API/mobile/desktop READMEs claim sharing/splitting/groups; receipt model includes `GroupId`, `PaidByUserID`, items, images, amount, and status. | No proof of multiple payers, consent, deterministic allocation, or Agent Household ledger semantics. |
| Atomicity/retry | Mobile create calls one `createReceiptWithFiles` and rebuilds multipart bytes; comment claims server atomicity. Saved-image loop retains successful partial uploads. | Server atomicity is unverified; neither behavior proves durable operation binding, exactly-once recovery, or cancellation. |
| Technologies/versions | Go directive `1.26.8`; desktop version `1.3.0`, Angular core `21.2.22`, TypeScript `~5.9.3`; Flutter dependency, mobile `2.6.0+28`, Dart SDK `>=3.7.0 <4.0.0`. | Declarations are not installed/runtime versions; exact Flutter version and API application version are not established here. |

## 6. F02: gap matrix against pinned Agent Household requirements

The review/upload papers and transaction model are design proposals, not implemented schemas; ACCEPTANCE explicitly keeps scenarios pending.

| Required seam | Upstream sample versus required state | Disposition |
|---|---|---|
| A09 provenance/custody | Image association/upload concepts exist; immutable original identity, source versions, attachment/page order, extraction lineage and verified coordinate transforms are not established. | Verify independently; preserve originals and append corrections within accepted retention policy. |
| A09 identities | Receipt model exposes one payer ID; owner, uploader, authenticated actor, and separately recorded payer contributions are distinct requirements. | No identity inference or forced single-payer mapping. |
| A10 uncertainty/finality | Text OCR/extraction claims do not establish material uncertainty, total consistency, or pre-tip/final distinction. | NEEDS_REVIEW remains explicit; no fabricated defaults. |
| Transaction/review boundary | Upstream receipt status and decimal amount are not Agent Household reconciliation/ledger semantics. | Draft never proves charge/payment, accepted expense/debt, allocation, or settlement. |
| A11 duplicate identities | Router `/duplicate` names a handler, not an evidence-based deduplication guarantee. | Namespaced source/version, lineage, purchase evidence and exact pair binding required; hashes alone never merge. |
| A18 authorization/privacy | Router uses auth middleware; implementation, attachment/export/tool protection and current household scope are unsampled. | Cross-household and authority-unavailable/revoked operations fail closed without existence disclosure. |
| A19 safe content/model disclosure | Client MIME filtering, image processing, subprocess OCR and debug files expose review questions, not certified safety. | Accepted types/limits/isolation/quarantine, injection-safe handling and destination consent block real processing. |
| A20 restore/custody | No sampled proof of isolated restore, identical projections/attachments, secret-free logs or suppression enforcement. | Future restore verification must include original hashes/order/mappings and current barriers. |
| A21 revocation/deletion | No sampled proof of unlink, retention/backup expiry, cancellation barriers or cleanup responsibility. | Policy unresolved; immutable outcomes are distinct from cleanup completion. |
| A22 phone/access/recovery | Mobile acquisition and desktop queue are useful concepts, not keyboard/screen-reader/correction/interruption evidence. | Later shared-contract and actual accessibility testing required; no selected visual design. |

- Preserve all named acceptance scope: **A09–A11 and A18–A22**, **R07-01–R07-07**, and **U07-01–U07-08** remain pending.
- R07-01/02/03/04/05/06/07 cover custody, revision concurrency, uncertainty, duplicate predicates/atomic pairs, injection/authority, proof recovery, and bounded money.
- U07-01/02/03/04/05/06/07/08 cover identity/mappings, unsafe content, bounded chunks/snapshots, uncertain extraction, authority/consent, crash recovery/restore, cancellation/deletion responsibility, and accessible review handoff.
- This evaluator can demonstrate selected synthetic logic only; it cannot satisfy real phone, upload validation, backup, accounting, or integration acceptance.

## 7. F03: exact proposed isolated verification seam

**The following four paths are proposed future files only: nonexistent, not written, and not implementation permission.** They define a future narrow allowlist, not an existing capability.

| Proposed path | Exclusive future role |
|---|---|
| `research/receipt_draft_seam/evaluate.py` | Independently written offline evaluator of synthetic evidence-to-draft predicates and simulated proof/state transitions. |
| `tests/fixtures/receipt_draft_seam/cases.json` | Hand-authored public synthetic inputs, expected observations, adversarial proof cuts, and explicit blocked cases. |
| `tests/test_receipt_draft_seam.py` | Executable assertions invoking only that evaluator with those fixtures; detect unintended effects/disclosures. |
| `docs/research/receipt-draft-seam-evaluation.md` | Boundary, requirement/case mapping, input limits, blocked schema fields, command/result evidence and non-acceptance limits. |

- Smallest boundary: synthetic versioned evidence and explicit uncertainty in; draft-only observations or fail-closed/UNKNOWN/blocked results out. No production import, persistence, ledger, upload, provider, authentication, checkout, or financial interfaces.
- No retailer/service/network/credentials, real files requiring decoding, real household data, copied upstream code, generated clients, dependency installation, or external model calls.
- Fixtures use only public synthetic labels, such as `synthetic:owner-A`, `synthetic:uploader-B`, `synthetic:payer-C`, two numbered pages, and invented minor-unit amounts.
- Exact wire schema, identifiers, digest/canonicalization algorithm, proof issuer qualification, coordinate representation, currency bounds, policy/error encodings and persistence/fencing implementation remain **undefined/blocked** until separately scoped. Semantic cases below do not select them.
- Future command proposal after separate approval: `python -m unittest discover -s tests -p test_receipt_draft_seam.py`; no command was run, and no result is claimed.
- Mapping convention below: **E** is the evaluator path, **F** the fixture path, **T** the test path, **D** the boundary-documentation path named above. Every case has F inputs, E evaluation, T assertions, and D traceability/blocker status.

| Synthetic case / requirements | Assertions mapped to E/F/T/D |
|---|---|
| S01 lineage/order/coordinates — A09; R07-01; U07-01/08 | F supplies two ordered originals and a corrected derived field; T asserts E preserves original identity, source version, page/attachment order and original-region references. Missing/unverified transform mapping stays blocked, never fabricated; D records coordinate-schema blocker. |
| S02 uncertainty/no posting — A10; R07-03/07; U07-04/08 | F independently varies low confidence, mismatched total, nonfinal/pre-tip bill, unknown currency/amount/payer and missing unpaid. T asserts E cannot reconcile material uncertainty or emit accepted expense/debt/payment/ledger effects; valid arithmetic alone grants none. D records unsupported bounds/refund rules. |
| S03 distinct identities — A09; U07-01 | F assigns different owner/uploader/actor/payer and an explicit unknown payer. T asserts E retains distinctions without substitution, debt assignment or paid inference; D distinguishes synthetic identity labels from accepted roles. |
| S04 duplicate evidence scope — A11; R07-04 | F covers same authoritative source version, revised lineage, two legitimate identical purchases and ambiguous photo/import; hash/text equality alone is insufficient. T asserts exact distinct endpoints/source versions/revisions, UNRESOLVED when qualification is blocked, no automatic accounting merge and immutable reversal history. |
| S05 pair atomicity/concurrency — R07-02/04 | F includes root C versus A/B, A4 versus A5, either-endpoint failure and racing corrections. T asserts no partial endpoint effects, no ignored third receipt, at most one simulated revision winner and unchanged original outcomes on retry. D marks transaction/fence realizability unproved. |
| S06 cross-household/revoked failclosed — A18/19/21; R07-05; U07-05/07 | F varies hidden object/operation existence under denied, unavailable or revoked authority and malicious receipt instructions. T asserts equal opaque outward responses, no protected output/action, no inferred authority or destination consent; D states this is not actual server authorization testing. |
| S07 UNKNOWN absence-proof — A20/22; R07-06; U07-06 | F separately varies original binding, effect absence/commit, terminal absence/existence, outcome, canonicalizer, step custody and fence. T asserts missing lookup/outcome proves no absence, UNKNOWN prevents replay/rebinding/new worker, and only positive required independent proofs permit original remaining work. |
| S08 immutable cancellation/deletion — A21; U07-07 | F covers cancel wins, target wins, pre/post-atomic crash cuts, deletion APPLIED with cleanup pending, delayed output, compatible/conflicting barriers and D1/B1/C1→D2/B2. T asserts immutable outcomes, suppression preservation, no staged publication, no reopened terminal command and no duplicated successor responsibility. D blocks policy/atomic implementation choices. |
| S09 safety/chunks/partial/restore/access — A19/20/22; U07-02/03/04/06/08 | F uses symbolic unsafe/oversize content, ranges 0–99 + 200–299, later 100–199, unpublished partials and restore/access observations. T asserts old completion remains INVALID, new snapshot needs distinct binding, unsafe/unknown policy blocks processing, and uncertainty/custody persist. D explicitly excludes real decoder, restore and accessibility proof. |

- Atomic successful effect/outcome transactions, exact-pair updates, durable original binding, independent effect/terminal/disposition proofs, current authority, suppression and nonduplicating cleanup custody remain required—not waived by simulation.
- Undefined policy must produce explicit blocked cases, not synthetic “passing” acceptance. Fake issuer/authority proof models cannot qualify real ingestion or grant permissions.

## 8. Blockers, owners, review and publication

| Blocker | Scope / accountable owner |
|---|---|
| #2 / SPEC-00 policy | Airy coordinates policy/security/financial reviewers; roles, authority, sharing, qualified issuers, consent/destinations, hosting, retention/deletion/backups and keys require accepted decisions. Unassigned specialist ownership must be explicitly assigned. |
| Interoperability/schema | Parent #9/spec and architecture reviewers: exact fields, source/coordinate mappings, currency bounds, canonicalization, storage/fences, atomic recovery and cancellation responsibilities. No guessed adapter mapping. |
| License/composition | Airy routes mobile grant clarification, file/dependency/image inventory and ambiguous combined-work/distribution analysis to appropriate maintainers/counsel before reuse. |
| Real acceptance | Parent #9: upload safety/OCR, phone visual/accessibility contract, actual recovery/restore and whole SPEC-07 integration under separate authorization. |
| Research admission | Independent reviewer must assess this complete v2 and all supplied full sources, including exact four-path boundary and every synthetic assertion; parent records exact verdict and unresolved findings. |

- Parent verifies every manifest SHA-256/git blob against saved exact fetch; reconciles badge redaction/source-display differences without inventing byte equality.
- Verify complete L01–L03/F01–F03/Q01–Q02 coverage, immutable citations, report custody/hash, readable line count, no private data/tokens, and original/report/review preservation.
- Publication requires a separate lease, ≤399 readable changed lines, full repository gates, independent publication review, fresh merge verification and exact published-blob custody.
- Research logic evidence is not real integration acceptance. No parent product acceptance, legal/adoption/publication approval, or closure is granted; **#9 and #2 remain OPEN**.

## 9. Q01: complete supplied source/hash manifest

Each entry gives immutable URL, SHA-256, Git blob, and supplied byte count where available. License-copy equality is supplied custody evidence, not independently recomputed here.

| Source / immutable URL | SHA-256 | Git blob | Bytes |
|---|---|---|---|
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/README.md | `ba1e1a3a54faabdd28c00fe6b58eb3c6789bf00fe32ec7ef9846363e10c816bc` | `bd9184ea616f4259e2f513705e69ecab2ef9b357` | 292 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/LICENSE | `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef` | `0ad25db4bd1d86c452db3f9602ccdbe172438f52` | 34523 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/README.md | `a809125d7d7ec9bbbb8c98597f86829eafddbae6ae15f6a5d64c4b2259bd0457` | `6b1f291af798db0ca205ba9086d2993f29c7a70e` | 1170 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/desktop/LICENSE | `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef` | `0ad25db4bd1d86c452db3f9602ccdbe172438f52` | 34523 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/desktop/README.md | `d117d5e37244045fd22f40e2f1e3c9cf469e756a90508b256f5dcd3e18230d9f` | `152c2c6ac20476fd9de91c3b3e59cfd70b3d7dac` | 1324 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/docker/LICENSE | `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef` | `0ad25db4bd1d86c452db3f9602ccdbe172438f52` | 34523 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/mobile/README.md | `9c2aad640c3c4c61fdcf8f7c53e87e5afdce19a3ed55b0aca47253e3cfbe3aa4` | `805b13b15651a14d56f562430598b12bdc49b08f` | 922 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/desktop/package.json | `d50966cd71e7094138811748705b5ddaff63cd1338b7ea8cc75e70875ef5fe46` | `3e9de10b2030f7ef004423c41882d72aee295b47` | 2310 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/go.mod | `03890e00252e1fc886cfd5bd465397011a25e636af293f43834e0f2913442ff8` | `b5d8f5aedad63ac6f7df0620841b9f0ed2c5c7b8` | 4517 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/mobile/pubspec.yaml | `24e7eb0e5acca85f4788b098900de09e1904d84274d88b20670fec8d929b7a8a` | `7a5e9dcfb0c84fe840e6de83222bdffc0c5c537a` | 7993 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/internal/models/receipt.go | `1c8b464e45d2b2499a13fd1ca20995574cfe608b80aaedf24945430ee89d11ac` | `6ff1c3827a9ca603e3ef562f94f9e4ac2dd8ed61` | 1532 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/internal/routers/receipt.go | `63399e4f26060083cb3ca0bb96dbd2928b766674a9b63e35938d00f56e366617` | `6bf07d68b9a4676bcc8fcf75654227664394fb9e` | 970 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/internal/services/ocr.go | `d0f2004127c37ab654dab946420e7a994c0b9c990731e093b4a3a7c6da4e6e22` | `7283987b838080579de4e46f8302b92f9b60e112` | 6095 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/api/internal/ai/ai_client.go | `60f744c54645d369f9c7a02f4c5cfce6b3f5b1ef747294b07e86e0e1a638fcab` | `8f8cdc837f7241e3fc985eeee7236b4afde2e8fa` | 150 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/mobile/lib/shared/functions/receipt_upload.dart | `e91c5406f5f62bb4c0b37a15fb97b9b9b4199fb56661cac8894dc89089ae82c8` | `d8aad59cc2108bfd4107442961c9ebf28462217b` | 10285 |
| https://github.com/Receipt-Wrangler/receipt-wrangler/blob/fc285d42d47e2338ac8d7723de83fca48153a3a5/desktop/src/receipts/upload-image/upload-image.component.ts | `9789ec261f11aa6bac53f4e09880414cc8314ec458c99148f2423f0a0949d98a` | `311ac3c11120f6718be6b0ff7af73c10e7ebac1e` | 2068 |
| https://github.com/mfethe1/agent-household/blob/0026aa2132b54c662261d072efee235307e56e49/docs/ACCEPTANCE.md | `c1a0a5cee61b86330f201759f5d26c6c783fbe9efb9299bf5e02982e6469cb0c` | `5df5c616fe49da93081937b6e9c35f3b3db54ba5` | Not supplied |
| https://github.com/mfethe1/agent-household/blob/0026aa2132b54c662261d072efee235307e56e49/docs/TRANSACTION_MODEL.md | `8a32f11d806d8fe18b3da73f084313103bb6eb8ce70125fddc07cc730ab092c7` | `f35b74bfe055cabe168786238bde6af7cdc4880c` | Not supplied |
| https://github.com/mfethe1/agent-household/blob/0026aa2132b54c662261d072efee235307e56e49/docs/specs/receipt-review-contract.md | `ae3fb1b49ff036eef6e58c52bfc61f22e070799a3fe09e99e4ccb764af143d85` | `80888546376b0cd114295558856b9401b53f561a` | Not supplied |
| https://github.com/mfethe1/agent-household/blob/0026aa2132b54c662261d072efee235307e56e49/docs/specs/receipt-upload-extraction-contract.md | `a072a43e89166fdf02c15d2d53b762aaaebc05c67d32ec40403c2cb8144cf5e6` | `30090b0b18f9576e251ba84d7ce6cc50e7826056` | Not supplied |

**Q02 disposition: fresh v2 UNREVIEWED / UNEXECUTED; independent verdict and parent publication verification required.**