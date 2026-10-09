# Single-record raw Target title — proposed paper

Status: proposed, no source lease or repository writes. Scope/size review does not certify tests, typing, mutations or product behavior; implementation requires independent scope ACCEPT and adopted clarifications. Rejected 601/674-line papers and this revision's original 457-line paper remain preserved read-only externally; none is reused as admitted source.

## Contract
`collect_record_title(record: object, expected_tcin: object) -> tuple[str, ...] | None` returns exact tuple/exact native strings. The shipped eight-ASCII-digit predicate runs first: invalid expected ID causes no record access or guard call; valid ID causes exactly one shipped guard call, rejection returns None. Root must be exact dict; unknown fields remain guard-validated.
Missing TCIN yields (); present non-exact-string TCIN yields None; arbitrary native nonmatching TCIN yields () regardless of missing/native-JSON title shape. Matching TCIN requires present exact-string title, otherwise None. Return raw empty/entities/whitespace/controls/Unicode/surrogate title unchanged, untrusted and not decoded, normalized or final-title validated.
Ordinary Exception returns None; KeyboardInterrupt/SystemExit propagate. No IO/coercion/logging/diagnostics/input mutation; tuple retains no document reference. Caller keeps input stable. Bounds cover materialized record subtree only, not module/page/allocation/snapshot/concurrent progress/post-preflight mutation.
Dependency clarification for adoption: shipped fixture exports `HostileObject`, imported `HostileObject as Hostile`; no fixture copied or changed. Shipped `probe_calls` observes real guard code only (no predicate-trace claim), current-thread synchronous guarantees/restoration limitations inherited.

## Consumer evidence inventory
- R01 `test_r01_facts_and_raw_strings`: exact facts/types, ordinary/leading-zero/missing/nonmatching IDs, arbitrary nonmatching strings and unchanged raw empty/entity/whitespace/control/Unicode/surrogates.
- R02 `test_r02_native_type_matrix`: named native TCIN/title rejection rows, ignored nonmatching title forms and missing matching/nonmatching titles, fresh nonaliased inputs.
- R03 `test_r03_invalid_ids_and_hostile_callbacks`: invalid length/ASCII/Unicode/bool/null/subclass/object IDs, valid leading zero, paired hostile record, native input unchanged and every shared callback counter zero; safe static labels.
- R04 `test_r04_guard_rejection_control_pairs`: real guardFalse/extractorNone versus guardTrue/('raw',) for malformed roots/subclass descendants/cycle/alias/nonfinite/oversized integer/total-text. Exact10**4096 reject versus10**4096-1 control; explicit record key/value total2_000_000 control versus+1 reject in ignored metadata.
- R05 `test_r05_silence_ownership_and_immutable_result`: valid/invalid stdout/stderr silence, deep equality/identities, exact immutable tuple/string, unknown metadata/sibling not surfaced.
- R06 `test_r06_real_guard_calls_and_trace_cleanup`: invalid IDs zero real guard calls, valid exactly one/raw, RuntimeError fail closed/cancellations propagate; normal subsequent recovery and original trace identity restored with outer cleanup. No mocked guard/production seam.
- R07 `test_r07_direct_dependency_wiring`: module/global binding identity, direct-import resolution and actual public-function calls, conservative shadow checks for stores/args/imports/nested definitions/exception names; no dead-import-text acceptance.

## R08 external mutation recipes
Each independent mutation starts from original source, exact old string must match once, compiled/imported/typed mutant must fail named committed assertions, not setup errors. Store manifests, hashes, commands/exits outside repository; baseline/final full suites pass and original source hash remains unchanged. No runner/mutant committed.
1. `if not is_target_tcin(expected_tcin):` → `if bool(is_target_tcin) and False:`; kill `test_r03_invalid_ids_and_hostile_callbacks` (native bad match).
2. `if not is_bounded_json_tree(record):` → `if bool(is_bounded_json_tree) and False:`; kill `test_r04_guard_rejection_control_pairs` (ignored nonfinite metadata).
3. `if type(tcin) is not str:` → `if type(tcin) is not str and type(tcin) is not bool:`; kill `test_r02_native_type_matrix` (boolean TCIN).
4. `if "title" not in mapping:\n            return None` → `if "title" not in mapping:\n            return ()`; kill `test_r02_native_type_matrix` (missing matching title).
5. `return (title,)` → `return (__import__("html").unescape(title),)`; kill `test_r01_facts_and_raw_strings` (literal entities).
6. `if not is_target_tcin(expected_tcin):` → `if bool(is_target_tcin) and not (type(expected_tcin) is str and len(expected_tcin) == 8 and all("0" <= c <= "9" for c in expected_tcin)):`; kill `test_r07_direct_dependency_wiring` (removed actual predicate call).

## R09 gates and publication
Exactly three new files: `agent_household/target_record_title.py`, `tests/test_target_record_title.py`, this document. Hash full contents, canonical external Ruff format/count complete additions+deletions <=399 before independent scope review. No minification/coverage trimming/partial commits; oversized artifacts rejected. Paper measurement is not execution.
After admission: Python3.11 `-B -m unittest discover -s tests -v` includes inherited48 and new record tests, no skips; canonical isolated Ruff py311 selects E,F,W,I,UP,B,A,C4,SIM,RUF,ANN plus full format check; strict Basedpyright full package/tests with external Python3.11 config and explicit interpreter, no exclusions; external-cache compileall; `git diff --check`/allowlist. Run six causal mutations, exact-head independent executed review, parent verification/publication, fresh merged full gates/hash/clean verification separately.

## Mandatory deferrals
No product caller yet; separately serialized module WIRE must connect producer. Module selection/container logic/ordering/multirecord late-invalid discard/64-65 occurrences deferred. ALL #33 F01-F12 wholewalker/fullpage bounds, paired root/depth/node/text, concurrent progress/post-preflight caps/aggregate paths/immutability/silence/walker invalidID/closure remain mandatory; record tests do not close walker obligations.
ALL #29 D01-D04 printable decoded validated title/conflicts/HTML transport, private/live selected-store offers/Costco/Amazon/private household/shared expenses remain deferred. #33/#29/#25/#23/#24 stay OPEN. No live adapter/purchase/private deployment/auth/install/runtime/provider change; record admission is not product acceptance.
